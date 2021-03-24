<template>
    <v-container class="col-6 centerContent">
        <h1 class="centerText">고객 등록</h1>
        <div class="col-6 centerContent">
            <div>
                <v-spacer></v-spacer>
                <div>
                    <img :src="imageUrl" style="border:0px; width:100%;" />
                </div>
                <v-row style="padding-top:20px;">
                    <v-spacer></v-spacer>
                    <p>{{ imageName }}</p>
                    <input ref="imageInput" type="file" hidden @change="onChangeImages" />
                    <v-btn type="button" @click="onClickImageUpload">이미지 업로드</v-btn>
                </v-row>
                <v-spacer></v-spacer>
            </div>
            <v-row style="margin:0; padding:0;">
                <v-text-field v-model="name" label="name" type="string" dark></v-text-field>
                <v-spacer></v-spacer>
                <v-text-field v-model="age" label="나이" type="number" dark></v-text-field>
            </v-row>
            <v-text-field v-model="interest" label="관심분야" type="string" dark></v-text-field>
            <v-text-field v-model="demand" label="요구사항" type="string" dark></v-text-field>
            <v-row style="margin:0; padding:0;">
                <v-spacer></v-spacer>
                <v-btn elevation="2" class="resetBtn" @click="resetInformation">초기화</v-btn>

                <v-btn elevation="2" class="registBtn">등록</v-btn>
            </v-row>
        </div>
    </v-container>
</template>

<script>
export default {
    data() {
        return {
            imageUrl: '',
            imageName: this.imageName,
            name: '',
            age: '',
            interest: '',
            demand: '',
        };
    },
    methods: {
        onClickImageUpload() {
            this.$refs.imageInput.click();
        },
        onChangeImages(e) {
            console.log(e.target.files);
            const file = e.target.files[0];
            this.imageUrl = URL.createObjectURL(file);
            this.imageName = file.name;
        },
        resetInformation() {
            console.log('resetInformation');
            this.name = '';
            this.age = '';
            this.interest = '';
            this.demand = '';
        },
    },
};
</script>

<style scoped>
@import '../assets/css/customerRegister.css';
</style>
