<template>
    <header>
        <v-row>
            <div class="logoBox" @click="goMain">
                <img src="@/assets/images/logo.png" alt="Logo" class="logoImg"/>
            </div>
            <v-spacer></v-spacer>
            <v-row class="menu col-3">
                <li class="col-4" @click="goAdminMain">관리자 페이지</li>
                <li class="col-4" @click="goCustomerRegister">고객 등록</li>
                <li class="col-4" @click="goCustomerModify">고객 정보 수정</li>
            </v-row>
        </v-row>
    </header>
</template>
<script>
export default {
    data() {
        return {};
    },
    methods: {
        goMain(){
            this.$router.push({name:'Cam'});
        },
        goAdminMain() {
            this.$router.push({ name: 'AdminMain' });
        },
        goCustomerRegister(){
            this.$router.push({ name:'CustomerRegister' });
        },
        goCustomerModify(){
            this.$router.push({name:'CustomerModify'});
        }
    },
};
</script>
<style scoped>
@import '../../assets/css/header.css';
</style>
