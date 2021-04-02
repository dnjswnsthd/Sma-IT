<template>
    <v-dialog v-model="dialogDelete" max-width="500px">
        <v-card>
            <p class="headTitle" style="color: black; text-align:center; padding-top: 10px; ">
                {{ item.name }}님의 고객정보를 삭제하시겠습니까?
            </p>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" text @click="closeDelete">Cancel</v-btn>
                <v-btn color="blue darken-1" text @click="deleteItemConfirm">OK</v-btn>
                <v-spacer></v-spacer>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script>
import http from '../../api/axios';
import swal from 'sweetalert';
export default {
    name: 'DeleteDialog',
    props: {
        dialogDelete: Boolean,
        item: Object,
    },
    methods: {
        closeDelete() {
            this.dialogDelete = false;
            this.$emit('closeDelete', this.item);
        },
        deleteItemConfirm() {
            console.log('here');
            http.delete(`/member/${this.item.uuid}`)
                .then((response) => {
                    console.log(response.data);
                    swal('삭제 되었습니다.', {
                        icon: 'success',
                    });
                    this.closeDelete();
                })
                .catch(() => {
                    swal('삭제 실패', {
                        icon: 'error',
                    });
                });
        },
    },
};
</script>
