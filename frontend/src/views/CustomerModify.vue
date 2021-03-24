<template>
    <v-container class="col-8 centerContent">
        <v-data-table :headers="headers" :items="customers" style="background:rgba(0,0,0,0)" dark>
            <template v-slot:top>
                <p class="modifyTitle">고객 정보 수정</p>
                <v-divider class="mx-4" inset vertical></v-divider>

                <v-spacer></v-spacer>
                <DeleteDialog :dialogDelete="dialogDelete" :item="editedItem"></DeleteDialog>
                <EditDialog :dialogEdit="dialogEdit" :item="editedItem"></EditDialog>
                <!-- <v-dialog v-model="dialogEdit" max-width="500px">
                    <v-card>
                        <v-card-text>
                            <v-container>
                                <img
                                    src="../assets/images/profile.png"
                                    alt="프로필 사진"
                                    style="width: 100%; padding-top: 10px;"
                                />
                                <v-row style="padding-top: 10px">
                                    <v-spacer></v-spacer>
                                    <v-col cols="12" sm="6" md="4">
                                        <v-text-field
                                            v-model="editedItem.name"
                                            label="name"
                                        ></v-text-field>
                                    </v-col>
                                    <v-spacer></v-spacer>
                                    <v-col cols="12" sm="6" md="4">
                                        <v-text-field
                                            v-model="editedItem.age"
                                            label="나이"
                                        ></v-text-field>
                                    </v-col>
                                    <v-spacer></v-spacer>
                                </v-row>
                                <v-row>
                                    <v-spacer></v-spacer>
                                    <v-col cols="12" sm="6" md="4">
                                        <v-text-field
                                            v-model="editedItem.rate"
                                            label="등급"
                                        ></v-text-field>
                                    </v-col>
                                    <v-spacer></v-spacer>
                                    <v-col cols="12" sm="6" md="4">
                                        <v-text-field
                                            v-model="editedItem.interest"
                                            label="관심품목"
                                        ></v-text-field>
                                    </v-col>
                                    <v-spacer></v-spacer>
                                </v-row>
                                <v-spacer></v-spacer>
                                <v-text-field
                                    v-model="editedItem.require"
                                    label="요구사항"
                                ></v-text-field>
                                <v-spacer></v-spacer>
                            </v-container>
                        </v-card-text>
                        <v-card-actions>
                            <v-spacer></v-spacer>
                            <v-btn color="black darken-1" text @click="close">
                                Cancel
                            </v-btn>
                            <v-btn color="black darken-1" text @click="save">
                                Save
                            </v-btn>
                        </v-card-actions>
                    </v-card>
                </v-dialog> -->
            </template>
            <template v-slot:item.actions="{ item }">
                <v-icon small class="mr-2" style="color:#fff;" @click="editItem(item)">
                    mdi-pencil
                </v-icon>
                <v-icon small style="color:#fff;" @click="deleteItem(item)">
                    mdi-delete
                </v-icon>
            </template>
            <template v-slot:no-data>
                <v-btn color="primary" @click="initialize">
                    Reset
                </v-btn>
            </template>
        </v-data-table>
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
        headers: [
            {
                text: '고객명',
                align: 'start',
                sortable: false,
                value: 'name',
            },
            { text: '나이', value: 'age' },
            { text: '등급', value: 'rate' },
            { text: '관심사', value: 'interest' },
            { text: '요구사항', value: 'require' },
            { text: '사진', value: 'picture' },
            { text: 'Actions', value: 'actions', sortable: false },
        ],
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
        defaultItem: {
            name: '',
            age: '',
            rate: 0,
            interest: 0,
            require: 0,
            picture: 0,
        },
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
