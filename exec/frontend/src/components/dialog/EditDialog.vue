<template>
    <v-dialog v-model="dialogEdit" max-width="500px">
        <v-card>
            <v-card-text>
                <v-container>
                    <img
                        :src="`data:image/jpg;base64,${item.customer_image}`"
                        style="width:100%;  height:100%;"
                        alt="customoer_image"
                    />
                    <v-row>
                        <v-col cols="12" sm="6" md="6">
                            <v-text-field v-model="item.name" label="name"></v-text-field>
                        </v-col>
                        <v-spacer></v-spacer>
                        <v-col cols="12" sm="6" md="6">
                            <v-text-field v-model="item.age" label="나이"></v-text-field>
                        </v-col>
                        <v-spacer></v-spacer>
                    </v-row>
                    <v-row>
                        <v-col cols="12" sm="6" md="12">
                            <v-text-field v-model="item.interests" label="관심품목"></v-text-field>
                        </v-col>
                        <v-spacer></v-spacer>
                    </v-row>
                    <v-row>
                        <v-col>
                            <v-text-field
                                v-model="item.requirements"
                                label="요구사항"
                            ></v-text-field>
                            <v-spacer></v-spacer>
                        </v-col>
                    </v-row>
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
    </v-dialog>
</template>

<script>
import http from '../../api/axios';
import swal from 'sweetalert';
import { mapState } from 'vuex';
export default {
    name: 'EditDialog',
    props: {
        dialogEdit: Boolean,
        item: Object,
    },
    computed: {
        ...mapState(['customerInfo']),
    },
    methods: {
        // close 버튼 클릭 시 고객 정보 수정 다이얼로그 닫고 부모에 수정된 값 전달
        close() {
            this.dialogEdit = false;
            this.$emit('close', this.item);
        },
        save() {
            // 고객 정보 수정 사항 서버에 반영
            http.put('/member/', this.item)
                .then((response) => {
                    console.log(response);
                    this.$store.commit('updateCustomerInfo', this.item);
                    this.close();
                })
                .catch(() => {
                    swal('실패', {
                        icon: 'error',
                    });
                });
        },
    },
};
</script>
