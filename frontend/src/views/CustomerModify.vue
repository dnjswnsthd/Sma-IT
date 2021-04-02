<template>
    <v-container class="col-8 centerContent">
        <p class="modifyTitle">고객 정보 수정</p>
        <v-divider class="mx-4" inset vertical></v-divider>

        <v-spacer></v-spacer>
        <v-row>
            <div v-for="(customer, index) in customers" :key="index">
                <div class="customInfoBox imgBox">
                    <v-col style="height:300px;"
                        ><img
                            :src="`data:image/jpg;base64,${customer.customer_image}`"
                            style="width:100%;  height:100%; display:block; margin:0 auto;"
                    /></v-col>
                    <br />
                    <hr />
                    <br />
                    <p>이름 : {{ customer.name }}</p>
                    <p>나이 : {{ customer.age }}</p>
                    <p>관심분야 : {{ customer.interests }}</p>
                    <p>요구사항 : {{ customer.requirements }}</p>
                    <hr />
                    <div style="text-align:center;">
                        <v-spacer></v-spacer>
                        <v-icon large class="mr-2" style="color:#fff;" @click="editItem(customer)">
                            mdi-pencil
                        </v-icon>
                        <v-icon large style="color:#fff;" @click="deleteItem(customer)">
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
        this.append_list();
        window.addEventListener('scroll', this.scroll);
    },
    destroyed() {
        window.removeEventListener('scroll', this.scroll);
    },
    mounted() {
        this.isLoading = false;
    },

    methods: {
        scroll() {
            let scrolledToBottom =
                document.documentElement.scrollTop + window.innerHeight ===
                document.documentElement.offsetHeight;
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
                    if (response.data.length >= this.limit) {
                        this.isLoading = true;
                        for (var i = 0; i < this.limit; i++) {
                            if (response.data.members[i].requirements == 'null')
                                response.data.members[i].requirements = '없음';
                            this.customers.push({
                                uuid: response.data.members[i].uuid,
                                name: response.data.members[i].name,
                                age: response.data.members[i].age,
                                interests: response.data.members[i].interests,
                                requirements: response.data.members[i].requirements,
                                image: response.data.members[i].uuid.image,
                                customer_image: response.data.images[i],
                            });
                        }
                        this.start += this.limit;
                        console.log(this.start);
                    } else {
                        for (i = 0; i < response.data.members.length; i++) {
                            if (response.data.members[i].requirements == 'null')
                                response.data.members[i].requirements = '없음';
                            this.customers.push({
                                uuid: response.data.members[i].uuid,
                                name: response.data.members[i].name,
                                age: response.data.members[i].age,
                                interests: response.data.members[i].interests,
                                requirements: response.data.members[i].requirements,
                                image: response.data.members[i].image,
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
.v-dialog {
    font-family: 'MapoFlowerIsland';
    color: #fff;
}
p {
    margin: 8px;
}
@import '../assets/css/customerModify.css';
</style>
