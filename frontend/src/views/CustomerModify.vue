<template>
    <v-container class="col-8 centerContent">
        <p class="modifyTitle">고객 정보 수정</p>
        <v-divider class="mx-4" inset vertical></v-divider>

        <v-spacer></v-spacer>
        <v-row>
            <div v-for="(item, index) in customers" :key="index" class="imgBox">
                <div class="customInfoBox">
                    <v-col>{{ item.picture }}</v-col>
                    <v-col>{{ item.name }}</v-col>
                    <v-col>{{ item.age }}</v-col>
                    <v-col>{{ item.rate }}</v-col>
                    <v-col>{{ item.interest }}</v-col>
                    <v-col>{{ item.require }}</v-col>
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
        <v-row>
            <v-col cols="12" lg="5">
                <hr />
            </v-col>
            <v-col cols="12" lg="2" style="text-align: center">
                <v-btn color="white accent-4" @click="moreView"> More </v-btn>
            </v-col>
            <v-col cols="12" lg="5">
                <hr />
            </v-col>
        </v-row>
    </v-container>
</template>
<script>
import DeleteDialog from '../components/dialog/DeleteDialog';
import EditDialog from '../components/dialog/EditDialog';

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
        limit: 4,
        total: 10,
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

    created() {
        this.initialize();
    },

    methods: {
        initialize() {
            this.customers = [
                {
                    name: '송원준',
                    age: '26',
                    rate: 'Diamond',
                    interest: '운동화',
                    require: '먼저 말 걸지 말아주세요. 문의 사항이 있으면 여쭤볼게요!',
                    picture: 0,
                },
                {
                    name: '조석준',
                    age: '29',
                    rate: 'Diamond',
                    interest: '맨투맨',
                    require: '먼저 말 거는게 힘들어요. 먼저 다가와주세요.',
                    picture: 0,
                },
                {
                    name: '조준형',
                    age: '26',
                    rate: 'Platinum',
                    interest: '후드티',
                    require: '신상 후드티에 관심이 많아요.',
                    picture: 0,
                },
                {
                    name: '김두상',
                    age: '27',
                    rate: 'Platinum',
                    interest: '양말',
                    require: '양말은 색깔별로 다 좋아요!',
                    picture: 0,
                },
                {
                    name: '천민주',
                    age: '27',
                    rate: 'Gold',
                    interest: '안경테',
                    require: '양말은 색깔별로 다 좋아요!',
                    picture: 0,
                },
                {
                    name: '천민주',
                    age: '27',
                    rate: 'Gold',
                    interest: '안경테',
                    require: '양말은 색깔별로 다 좋아요!',
                    picture: 0,
                },
            ];
        },

        editItem(item) {
            console.log(item);
            this.editedIndex = this.customers.indexOf(item);
            this.editedItem = Object.assign({}, item);
            this.dialogEdit = true;
        },

        deleteItem(item) {
            console.log(item);
            this.editedIndex = this.customers.indexOf(item);
            this.editedItem = Object.assign({}, item);
            this.dialogDelete = true;
        },
        closeDelete() {
            this.dialogDelete = false;
        },
        close() {
            this.dialogEdit = false;
        },
        moreView() {
            this.limit += 5;
            this.customers.push(
                {
                    name: '송원준',
                    age: '26',
                    rate: 'Diamond',
                    interest: '운동화',
                    require: '먼저 말 걸지 말아주세요. 문의 사항이 있으면 여쭤볼게요!',
                    picture: '../../assets/images/profile.png',
                },
                {
                    name: '조석준',
                    age: '29',
                    rate: 'Diamond',
                    interest: '맨투맨',
                    require: '먼저 말 거는게 힘들어요. 먼저 다가와주세요.',
                    picture: 0,
                },
                {
                    name: '조준형',
                    age: '26',
                    rate: 'Platinum',
                    interest: '후드티',
                    require: '신상 후드티에 관심이 많아요.',
                    picture: 0,
                },
                {
                    name: '김두상',
                    age: '27',
                    rate: 'Platinum',
                    interest: '양말',
                    require: '양말은 색깔별로 다 좋아요!',
                    picture: 0,
                },
                {
                    name: '천민주',
                    age: '27',
                    rate: 'Gold',
                    interest: '안경테',
                    require: '양말은 색깔별로 다 좋아요!',
                    picture: 0,
                },
                {
                    name: '조준형',
                    age: '26',
                    rate: 'Platinum',
                    interest: '후드티',
                    require: '신상 후드티에 관심이 많아요.',
                    picture: 0,
                }
            );
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
