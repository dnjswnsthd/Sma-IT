<template>
    <header>
        <v-row>
            <div class="logoBox" @click="goMain">
                <img src="@/assets/images/logo.png" alt="Logo" class="logoImg" />
            </div>
            <v-spacer></v-spacer>
            <!--페이지 이동 확인을 위해 adminHeader와 동일하게 제작.-->
            <v-row class="menu col-6">
                <li @click="goAdminMain">관리자 페이지</li>
                <li @click="goCustomerRegister">고객 등록</li>
                <li @click="goCustomerModify">고객 정보 수정</li>
                <li @click="goCamPayment">결제 화면 보기</li>
                <li @click="goCamSatisfied">만족도화면보기</li>
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
        goMain() {
            this.$router.push({ name: 'Main' });
        },
        goCamSatisfied() {
            this.$router.push({ name: 'CamSatisfied' });
        },
        goCamPayment() {
            this.$router.push({ name: 'CamPayment' });
        },
        goAdminMain() {
            this.$router.push({ name: 'AdminMain' });
        },
        goCustomerRegister() {
            this.$router.push({ name: 'CustomerRegister' });
        },
        goCustomerModify() {
            this.$router.push({ name: 'CustomerModify' });
        },
    },
};
</script>

<style scoped>
@import '../../assets/css/header.css';
</style>
