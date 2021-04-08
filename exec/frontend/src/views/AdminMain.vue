<template>
    <v-container>
        <div class="mx-auto" max-width="1920">
            <h2 class="col-11 centerContent">
                현재 방문 고객 현황
                <span>현재 고객 수 : {{ getCustomerInfo.length }}</span>
            </h2>
            <!-- 좌우 이동을 위한 슬라이드 -->
            <v-slide-group class="my-slider" center-active dark>
                <v-slide-item
                    v-for="(customer, index) in getCustomerInfo"
                    :key="index"
                    v-slot="{ active, toggle }"
                >
                    <!-- 고객 정보 카드 -->
                    <SatisfyCard
                        :customer="customer"
                        :active="active"
                        :toggle="toggle"
                    ></SatisfyCard>
                </v-slide-item>
            </v-slide-group>
        </div>
    </v-container>
</template>
<script>
import { mapGetters } from 'vuex';

import SatisfyCard from '../components/SatisfyCard';

export default {
    name: 'AdminMain',
    components: {
        SatisfyCard,
    },
    computed: {
        ...mapGetters(['getCustomerInfo']),
    },
};
</script>
<style scoped>
@import '../assets/css/adminMain.css';
</style>
