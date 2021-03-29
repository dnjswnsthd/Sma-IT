<template>
    <v-container class="col-8 centerContent">
        <p class="modifyTitle">고객 정보 수정</p>
        <v-divider class="mx-4" inset vertical></v-divider>

        <v-spacer></v-spacer>
        <v-row>
            <div v-for="(customer, index) in customers" :key="index" class="imgBox">
                <div class="customInfoBox">
                    <v-col
                        ><img :src="customer.customer_picture" style="width:100%; margin:0 auto;"
                    /></v-col>
                    <v-col>{{ customer.customer_name }}</v-col>
                    <v-col>{{ customer.customer_age }}</v-col>
                    <v-col>관심분야 : {{ customer.customer_interest }}</v-col>
                    <v-col>요구사항 : {{ customer.customer_require }}</v-col>
                    <div>
                        <v-spacer></v-spacer>
                        <v-icon small class="mr-2" style="color:#fff;" @click="editItem(item)">
                            mdi-pencil
                        </v-icon>
                        <v-icon small style="color:#fff;" @click="deleteItem(item)">
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

import http from '../api/axios';

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
            rate: 0,
            interest: 0,
            require: 0,
            picture: 0,
        },
        start: 0,
        limit: 6,
        isLoading: true,
    }),

    computed: {
        formTitle() {
            return this.editedIndex === -1 ? 'New Item' : 'Edit Item';
        },
    },

    watch: {
        dialog(val) {
            val || this.close();
        },
        dialogDelete(val) {
            val || this.closeDelete();
        },
    },

    // created() {
    //     this.initialize();
    // },
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
        append_list() {
            http.get(`/api/member/`, {
                params: {
                    start: this.start,
                    limit: this.limit,
                },
            })
                .then((response) => {
                    if (response.data.length >= this.limit) {
                        this.isLoading = true;
                        for (var i = 0; i < this.limit; i++) {
                            if (response.data[i].requirements == 'null')
                                response.data[i].requirements = '없음';
                            this.customers.push({
                                customer_name: response.data[i].name,
                                customer_age: response.data[i].age,
                                customer_interest: response.data[i].interests,
                                customer_require: response.data[i].requirements,
                                customer_picture: response.data[i].image,
                            });
                        }
                        this.start += this.limit;
                        console.log(this.start);
                    } else {
                        for (i = 0; i < response.data.length; i++) {
                            if (response.data[i].requirements == 'null')
                                response.data[i].requirements = '없음';
                            this.customers.push({
                                customer_name: response.data[i].name,
                                customer_age: response.data[i].age,
                                customer_interest: response.data[i].interests,
                                customer_require: response.data[i].requirements,
                                customer_picture: response.data[i].image,
                            });
                        }
                        this.start += this.limit;
                        console.log(this.start);
                        this.isLoading = false;
                    }
                })
                .catch(() => {
                    alert('회원 정보가 더 이상 존재하지 않습니다.');
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
@import '../assets/css/customerModify.css';
</style>
