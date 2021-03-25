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
export default {
    name: 'DeleteDialog',
    props: {
        dialogDelete: Boolean,
        item: Object,
    },
    methods: {
        closeDelete() {
            this.dialogDelete = false;
            this.$emit('closeDelete');
            this.$nextTick(() => {
                this.editedItem = Object.assign({}, this.defaultItem);
                this.editedIndex = -1;
            });
        },
        deleteItemConfirm() {
            this.customers.splice(this.editedIndex, 1);
            this.closeDelete();
        },
    },
};
</script>
