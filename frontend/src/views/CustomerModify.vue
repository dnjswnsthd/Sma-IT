<template>
    <v-container style="padding-bottom:80px;">
        <p class="modifyTitle">고객 정보 수정</p>
        <v-divider class="mx-4" inset vertical></v-divider>

        <v-spacer></v-spacer>
        <v-row>
            <div v-for="(customer, index) in customers" :key="index" class="col-4">
                <div class="imgBox">
                    <div class="imgOutBox">
                        <img :src="`data:image/jpg;base64,${customer.customer_image}`" />
                    </div>

                    <div class="divider"></div>
                    <div class="infoBox">
                        <p>이름 : {{ customer.name }}</p>
                        <p>나이 : {{ customer.age }}</p>
                        <p>관심분야 : {{ customer.interests }}</p>
                        <p>요구사항 : {{ customer.requirements }}</p>
                        <p>입장시간 : {{ customer.start_visit }}</p>
                        <p>퇴장시간 : {{ customer.end_visit }}</p>
                    </div>
                    <div class="divider"></div>
                    <div class="btnBox">
                        <v-spacer></v-spacer>
                        <v-icon large class="mr-2" @click="editItem(customer)">
                            mdi-pencil
                        </v-icon>
                        <v-icon large @click="deleteItem(customer)">
                            mdi-delete
                        </v-icon>
                    </div>
                </div>
            </div>
        </v-row>
        <DeleteDialog
            :dialogDelete="dialogDelete"
            :item="editedItem"
            @closeDelete="closeDelete"
        ></DeleteDialog>
        <EditDialog :dialogEdit="dialogEdit" :item="editedItem" @close="close"></EditDialog>
    </v-container>
</template>
<script>
import DeleteDialog from '../components/dialog/DeleteDialog';
import EditDialog from '../components/dialog/EditDialog';
import swal from 'sweetalert';
import http from '../api/axios';
import { mapState } from 'vuex';
export default {
    components: {
        DeleteDialog,
        EditDialog,
    },
    data: () => ({
        dialog: false,
        dialogEdit: false,
        dialogDelete: false,
        customers: [],
        editedIndex: -1,
        editedItem: {
            name: '',
            age: '',
            interests: 0,
            requirements: 0,
            customer_image: '',
        },
        start: 0,
        limit: 6,
        isLoading: true,
    }),
    computed: {
        formTitle() {
            return this.editedIndex === -1 ? 'New Item' : 'Edit Item';
        },
        ...mapState(['customerInfo']),
    },
    watch: {
        dialog(val) {
            val || this.close();
        },
        dialogDelete(val) {
            val || this.closeDelete();
        },
    },
    created() {
        console.log(this.isLoading);
        this.append_list();
        window.addEventListener('scroll', this.scroll);
    },
    destroyed() {
        window.removeEventListener('scroll', this.scroll);
    },

    methods: {
        scroll() {
            // scrollTop
            // 요소의 상단에서 맨 위에 보이는 콘텐츠 까지의 거리를 측정 한 것입니다 .
            // 요소의 콘텐츠가 수직 스크롤바를 생성하지 않는 경우 해당 scrollTop값은 0입니다.

            // offsetHeight
            // padding이나 border등을 모두 포함한 요소의 높이.
            let scrolledToBottom =
                document.documentElement.scrollTop + window.innerHeight ===
                document.documentElement.offsetHeight;
            // console.log('scrollTop : ' + document.documentElement.scrollTop);
            // console.log('innerHeight : ' + window.innerHeight);
            // console.log('offsetHeight : ' + document.documentElement.offsetHeight);
            // console.log('scrolledToBottom : ' + scrolledToBottom);
            console.log(this.isLoading);

            if (this.isLoading && scrolledToBottom) {
                this.isLoading = true;
                setTimeout(this.append_list, 1000);
            }
        },
        editItem(item) {
            console.log('item');
            this.editedIndex = this.customers.indexOf(item);
            this.editedItem = Object.assign({}, item);
            this.dialogEdit = true;
        },

        deleteItem(item) {
            // console.log(item);
            this.editedIndex = this.customers.indexOf(item);
            this.editedItem = Object.assign({}, item);
            console.log(this.editedItem);
            this.dialogDelete = true;
        },
        closeDelete(item) {
            this.dialogDelete = false;
            for (var i = 0; i < this.customers.length; i++)
                if (this.customers[i].uuid == item.uuid) this.customers.splice(i, 1);

            // location.href = '/customerModify';
        },
        close(item) {
            this.dialogEdit = false;
            for (var i = 0; i < this.customers.length; i++)
                if (this.customers[i].uuid == item.uuid) this.customers[i] = item;
        },
        append_list() {
            http.get(`/member/`, {
                params: {
                    start: this.start,
                    limit: this.limit,
                },
            })
                .then((response) => {
                    if (response.data.members.length >= this.limit) {
                        console.log('data : ' + response.data.members);
                        this.isLoading = true;
                        for (var i = 0; i < this.limit; i++) {
                            this.customers.push({
                                uuid: response.data.members[i].uuid,
                                name: response.data.members[i].name,
                                age: response.data.members[i].age,
                                interests: response.data.members[i].interests,
                                requirements: response.data.members[i].requirements,
                                image: response.data.members[i].image,
                                start_visit: response.data.members[i].start_visit,
                                end_visit: response.data.members[i].end_visit,
                                customer_image: response.data.images[i],
                            });
                        }
                        this.start += this.limit;
                        console.log(this.start);
                    } else {
                        for (i = 0; i < response.data.members.length; i++) {
                            this.customers.push({
                                uuid: response.data.members[i].uuid,
                                name: response.data.members[i].name,
                                age: response.data.members[i].age,
                                interests: response.data.members[i].interests,
                                requirements: response.data.members[i].requirements,
                                image: response.data.members[i].image,
                                start_visit: response.data.members[i].start_visit,
                                end_visit: response.data.members[i].end_visit,
                                customer_image: response.data.images[i],
                            });
                        }
                        this.start += this.limit;
                        console.log(this.start);
                        this.isLoading = false;
                    }
                })
                .catch(() => {
                    swal('회원 정보가 더 이상 존재하지 않습니다.', {
                        icon: 'error',
                    });
                });
        },
    },
};
</script>
<style scoped>
@import '../assets/css/customerModify.css';
</style>
