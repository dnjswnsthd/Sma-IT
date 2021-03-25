<template>
    <v-dialog v-model="dialogEdit" max-width="500px">
        <v-card>
            <v-card-text>
                <v-container>
                    <img
                        src="../../assets/images/profile.png"
                        alt="프로필 사진"
                        style="width: 100%; padding-top: 10px;"
                    />
                    <v-row style="padding-top: 10px">
                        <v-spacer></v-spacer>
                        <v-col cols="12" sm="6" md="4">
                            <v-text-field v-model="item.name" label="name"></v-text-field>
                        </v-col>
                        <v-spacer></v-spacer>
                        <v-col cols="12" sm="6" md="4">
                            <v-text-field v-model="item.age" label="나이"></v-text-field>
                        </v-col>
                        <v-spacer></v-spacer>
                    </v-row>
                    <v-row>
                        <v-spacer></v-spacer>
                        <v-col cols="12" sm="6" md="4">
                            <v-text-field v-model="item.rate" label="등급"></v-text-field>
                        </v-col>
                        <v-spacer></v-spacer>
                        <v-col cols="12" sm="6" md="4">
                            <v-text-field v-model="item.interest" label="관심품목"></v-text-field>
                        </v-col>
                        <v-spacer></v-spacer>
                    </v-row>
                    <v-spacer></v-spacer>
                    <v-text-field v-model="item.require" label="요구사항"></v-text-field>
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
    </v-dialog>
</template>

<script>
export default {
    name: 'EditDialog',
    props: {
        dialogEdit: Boolean,
        item: Object,
    },
    methods: {
        close() {
            this.dialogEdit = false;
            this.$emit('close');
            this.$nextTick(() => {
                this.item = Object.assign({}, this.defaultItem);
                this.editedIndex = -1;
            });
        },
        save() {
            if (this.editedIndex > -1) {
                Object.assign(this.customers[this.editedIndex], this.item);
            } else {
                this.customers.push(this.item);
            }
            this.close();
        },
    },
};
</script>
