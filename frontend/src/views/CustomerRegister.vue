<template>
    <v-container class="col-6 centerContent">
        <p class="centerText registerTitle">고객 등록</p>
        <div class="col-6 centerContent">
            <div>
                <v-spacer></v-spacer>
                <div class="pb-5">
                    <img v-if="imageUrl == ''" :src="imageUrl" />
                    <img v-else :src="imageUrl" class="profileImg" />
                </div>
                <v-row>
                    <v-spacer></v-spacer>
                    <p class="profileName">{{ imageName }}</p>

                    <input ref="imageInput" type="file" hidden @change="onChangeImages" />
                    <v-btn type="button" @click="onClickImageUpload">이미지 업로드</v-btn>
                </v-row>
                <v-spacer></v-spacer>
            </div>

            <v-row>
                <v-text-field
                    v-model="member.name"
                    label="name"
                    type="string"
                    dark
                    class="nameField"
                ></v-text-field>
                <v-spacer></v-spacer>
                <v-text-field
                    v-model="member.age"
                    label="나이"
                    type="number"
                    dark
                    class="ageField"
                ></v-text-field>
            </v-row>
            <v-text-field
                v-model="member.interests"
                label="관심분야"
                type="string"
                dark
            ></v-text-field>
            <v-text-field
                v-model="member.requirements"
                label="요구사항"
                type="string"
                dark
            ></v-text-field>
            <v-row>
                <v-spacer></v-spacer>
                <button class="resetBtn" @click="resetInformation">초기화</button>

                <button class="registBtn" @click="registInformation">등록</button>
            </v-row>
        </div>
    </v-container>
</template>

<script>
import http from '../api/axios';
import swal from 'sweetalert';
export default {
    data() {
        return {
            imageName: this.imageName,
            imageFile: '',
            imageUrl: '',
            member: {
                name: '',
                age: '',
                interests: '',
                requirements: '',
                image: 'test.jpg',
            },
        };
    },
    methods: {
        onClickImageUpload() {
            this.$refs.imageInput.click();
        },
        onChangeImages(e) {
            console.log(e.target.files);
            const file = e.target.files[0];
            this.imageFile = file;
            this.imageUrl = URL.createObjectURL(file);
            this.imageName = file.name;
        },
        resetInformation() {
            console.log('resetInformation');
            this.name = '';
            this.age = '';
            this.interests = '';
            this.requirements = '';
        },
        registInformation() {
            let formData = new FormData();
            formData.append('file', this.imageFile);
            http.post('/member/', this.member)
                .then((response) => {
                    this.imageName = response.data.image;
                    http.post(`/member/image/${this.imageName}`, formData)
                        .then(() => {
                            swal('등록 성공!', {
                                icon: 'success',
                            });
                            this.$router.push({ name: 'Cam' });
                        })
                        .catch(() => {
                            swal('등록 실패!', {
                                icon: 'error',
                            });
                        });
                })
                .catch((response) => {
                    swal('등록 실패!', {
                        icon: 'error',
                    });
                    console.log(response);
                });
        },
    },
};
</script>

<style scoped>
@import '../assets/css/customerRegister.css';
</style>
