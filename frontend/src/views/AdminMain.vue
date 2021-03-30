<template>
    <v-container>
        <div class="mx-auto" max-width="1920" style="margin-top:50px;">
            <h2 class="adminTitle col-11 centerContent">
                현재 방문 고객 현황 <span>현재 고객 수 : {{ getCustomerInfo.length }} </span>
            </h2>
            <v-slide-group class="my-slider" center-active dark>
                <v-slide-item
                    v-for="customer in getCustomerInfo"
                    :key="customer"
                    v-slot="{ active, toggle }"
                >
                    <v-card
                        :color="active ? '#192537' : '#192537'"
                        class="ma-4"
                        height="600"
                        width="380"
                        @click="toggle"
                    >
                        <div class="fill-height imgBox">
                            <div class="firstBox">
                                <div class="col-6 customInfoBox">
                                    <p class="imgArea">이미지영역</p>
                                </div>
                                <div class="col-6 customInfoBox">
                                    <p>이름 : {{ customer.name }}</p>
                                    <p>나이 : {{ customer.age }}세</p>
                                    <p>성별 : {{ customer.sex }}</p>
                                </div>
                            </div>

                            <div class="secondBox">
                                <p>등급 : Diamond</p>
                                <p>관심상품 : 없음</p>
                                <p>
                                    요구사항 <br />
                                    먼저 말 걸지 말아주세요.<br />
                                    문의 사항이 있으면 여쭤볼게요!
                                </p>
                                <button class="satisfiedBtn" @click="goCamSatisfied">
                                    => 만족도 확인
                                </button>
                            </div>
                            <div class="thirdBox">
                                <p>입장시간 : sadfdf</p>
                                <p>퇴장시간 : 퇴장전</p>
                            </div>
                        </div>
                    </v-card>
                </v-slide-item>
            </v-slide-group>
        </div>
    </v-container>
</template>
<script>
import { mapGetters } from 'vuex';

export default {
    data() {
        return {
            customers: [],
        };
    },
    computed: {
        ...mapGetters(['getCustomerInfo']),
    },
    methods: {
        goCamSatisfied() {
            this.$router.push({ name: 'CamSatisfied' });
        },
    },
};
</script>
<style scoped>
@import '../assets/css/adminMain.css';
.v-application p {
    margin: 0;
}
.secondBox p {
    margin-bottom: 16px;
}
</style>
