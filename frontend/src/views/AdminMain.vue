<template>
    <v-container>
        <h2>현재 방문 고객 현황 <span>현재 고객 수 : 6명 </span></h2>
        <div class="mx-auto" max-width="1920" style="margin-top:50px;">
            <v-slide-group class="pa-4 my-slider" center-active dark>
                <v-slide-item v-for="n in 15" :key="n" v-slot="{ active, toggle }">
                    <v-card
                        :color="active ? 'primary' : 'grey'"
                        class="ma-4"
                        height="600"
                        width="400"
                        @click="toggle"
                    >
                        <div class="fill-height">
                            <div class="firstBox">
                                <div class="col-6 customInfoBox">
                                    <p>이미지영역</p>
                                </div>
                                <div
                                    class="col-6 customInfoBox"
                                    
                                >
                                    <p>준형갓</p>
                                    <p>25세</p>
                                    <p>남성</p>
                                </div>
                            </div>
                            <div class="secondBox">
                                <p>등급 : Diamond</p>
                                <p>관심상품 : 없음</p>
                                <p>
                                    요구사항 <br />
                                    먼저 말 걸지 말아주세요. 문의 사항이 있으면 여쭤볼게요!
                                </p>
                                <p>=> <v-btn @click="goCamSatisfied">만족도확인</v-btn></p>
                            </div>
                            <div class="thirdBox">
                                <p>입장시간 : 2021.03.04 19:36</p>
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
export default {
    data(){
        return{

        }
    },
    methods:{
        goCamSatisfied(){
            this.$router.push({name:'CamSatisfied'});
        }
    }
};
</script>
<style scoped>
@import '../assets/css/adminMain.css';

</style>
