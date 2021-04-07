<template>
    <div>
        <v-card
            :color="active ? '#1D1C22' : '#1D1C22'"
            class="ma-4 imgBox"
            height="600"
            width="380"
            @click="toggle"
            style="margin:0 auto;"
        >
            <div>
                <div class="firstBox">
                    <v-row>
                        <div class="profileBox">
                            <img :src="`data:image/jpg;base64,${customer.image}`" />
                        </div>

                        <div class="customerInfoBox">
                            <div class="customerInfoInBox">
                                <p>이름 : {{ customer.name }}</p>
                                <br />
                                <p>나이 : {{ customer.age }}세</p>
                            </div>
                        </div>
                    </v-row>
                </div>
                <div class="divider"></div>
                <div class="secondBox">
                    <div class="secondTopBox">
                        <p>관심상품 : {{ customer.interests }}</p>
                        <p>
                            요구사항 :
                            {{ customer.requirements }}
                        </p>
                    </div>
                    <div class="divider"></div>

                    <v-dialog v-model="satisfyDialog" width="500">
                        <template v-slot:activator="{ on, attrs }">
                            <button
                                class="satisfiedBtn"
                                v-bind="attrs"
                                v-on="on"
                                @click="goCamSatisfied(customer.uuid)"
                            >
                                => 최근 만족도 확인 &lt;=
                            </button>
                        </template>

                        <v-card>
                            <!-- 만족도 그래프 그리기 -->
                            <Chart
                                :id="'uuid_' + customer.uuid"
                                :labels="labels"
                                :data="data"
                                style=" border:1px solid #fff;"
                            ></Chart>
                            <v-divider></v-divider>
                            <v-card-actions>
                                <v-spacer></v-spacer>
                                <v-btn color="primary" text @click="satisfyDialog = false">
                                    닫기
                                </v-btn>
                            </v-card-actions>
                        </v-card>
                    </v-dialog>
                </div>
                <div class="divider"></div>
                <div class="thirdBox">
                    <p>입장시간 : {{ customer.visit_start }}</p>
                    <p>퇴장시간 : 퇴장전</p>
                </div>
            </div>
        </v-card>
    </div>
</template>

<script>
import Chart from './Chart';
import swal from 'sweetalert';
import http from '../api/axios';

export default {
    name: 'SatisfyCard',
    components: {
        Chart,
    },
    props: {
        customer: Object,
        active: Boolean,
        toggle: Function,
    },
    data() {
        return {
            emotion: [],
            satisfyDialog: false,
            // 고객 만족도 라벨
            labels: [
                'anger',
                'contempt',
                'disgust',
                'fear',
                'happiness',
                'neutral',
                'sadness',
                'surprise',
            ],
            // 고객 만족도 데이터
            data: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        };
    },
    methods: {
        goCamSatisfied(uuid) {
            console.log('uuid : ' + uuid);
            http.get(`/member/emotion/${uuid}`)
                .then(({ data }) => {
                    // 현재 서버에 저장된 모든 만족도를 가져와 가장 최근것만 보여줌
                    let emo = [
                        data[data.length - 1].anger,
                        data[data.length - 1].contempt,
                        data[data.length - 1].disgust,
                        data[data.length - 1].fear,
                        data[data.length - 1].happiness,
                        data[data.length - 1].neutral,
                        data[data.length - 1].sadness,
                        data[data.length - 1].surprise,
                    ];
                    this.data = emo;
                })
                .catch(() => {
                    swal('서버에러 발생!', {
                        icon: 'error',
                    });
                });
        },
    },
};
</script>
