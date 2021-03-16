<template>
<v-container class="col-8 centerContent">
    <v-data-table
      :headers="headers"
      :items="desserts"
      sort-by="calories"
      style="background:rgba(0,0,0,0)"
      dark
    >
      <template v-slot:top>
        
          <p class="modifyTitle">고객 정보 수정</p>
          <v-divider
            class="mx-4"
            inset
            vertical
          ></v-divider>
          
          <v-spacer></v-spacer>

          
          <v-dialog v-model="dialogDelete" max-width="500px">
            <v-card>
              <v-card-title class="headline">Are you sure you want to delete this item?</v-card-title>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" text @click="closeDelete">Cancel</v-btn>
                <v-btn color="blue darken-1" text @click="deleteItemConfirm">OK</v-btn>
                <v-spacer></v-spacer>
              </v-card-actions>
            </v-card>
          </v-dialog>
        
      </template>
      <template v-slot:item.actions="{ item }">
        <v-icon
          small
          class="mr-2"
          style="color:#fff;"
          @click="editItem(item)"
        >
          mdi-pencil
        </v-icon>
        <v-icon
          small
          style="color:#fff;"
          @click="deleteItem(item)"
        >
          mdi-delete
        </v-icon>
      </template>
      <template v-slot:no-data>
        <v-btn
          color="primary"
          @click="initialize"
        >
          Reset
        </v-btn>
      </template>
    </v-data-table>
</v-container>
</template>
<script>
  export default {
    data: () => ({
      dialog: false,
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
      desserts: [],
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
      formTitle () {
        return this.editedIndex === -1 ? 'New Item' : 'Edit Item'
      },
    },

    watch: {
      dialog (val) {
        val || this.close()
      },
      dialogDelete (val) {
        val || this.closeDelete()
      },
    },

    created () {
      this.initialize()
    },

    methods: {
      initialize () {
        this.desserts = [
          { 
            name: '송원준',
            age: '26',
            rate: 'Diamond',
            interest: '운동화',
            require: '먼저 말 걸지 말아주세요. 문의 사항이 있으면 여쭤볼게요!',
            picture: 0,
          },
          { 
            name: '조석준ㄴ',
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
        ]
      },

      editItem (item) {
        this.editedIndex = this.desserts.indexOf(item)
        this.editedItem = Object.assign({}, item)
        this.dialog = true
      },

      deleteItem (item) {
        this.editedIndex = this.desserts.indexOf(item)
        this.editedItem = Object.assign({}, item)
        this.dialogDelete = true
      },

      deleteItemConfirm () {
        this.desserts.splice(this.editedIndex, 1)
        this.closeDelete()
      },

      close () {
        this.dialog = false
        this.$nextTick(() => {
          this.editedItem = Object.assign({}, this.defaultItem)
          this.editedIndex = -1
        })
      },

      closeDelete () {
        this.dialogDelete = false
        this.$nextTick(() => {
          this.editedItem = Object.assign({}, this.defaultItem)
          this.editedIndex = -1
        })
      },

      save () {
        if (this.editedIndex > -1) {
          Object.assign(this.desserts[this.editedIndex], this.editedItem)
        } else {
          this.desserts.push(this.editedItem)
        }
        this.close()
      },
    },
  }
</script>
<style scoped>
    @import '../assets/css/customerModify.css';
</style>