<template>
    <v-container style="padding-top: 40px">
        <v-spacer></v-spacer>
        <v-row class="wrapBox">
            <div class="col-3" style="padding-top: 200px;">
                <p class="introduceMessage" style="padding-top:20px;">
                    버튼을 눌러<br />합계를 확인하세요.
                </p>
                <v-img
                    @mouseover="domouseover_won"
                    @click="checkTotal"
                    v-if="!won_c"
                    :src="require('../assets/images/won(w).png')"
                    class="wonImage"
                ></v-img>
                <v-img
                    @click="checkTotal"
                    @mouseout="domouseout_won"
                    class="wonImage"
                    v-else
                    :src="require('../assets/images/won.png')"
                ></v-img>
                <p style="font-size: 30px; text-align: center; padding-top: 20px;">{{ total }}</p>
            </div>
            <div class="col-6 cambox">
                <vue-web-cam
                    ref="webcam"
                    :device-id="deviceId"
                    style="margin-top: 70px; "
                    width="100%"
                    height="580px"
                    @stopped="onStopped"
                    @error="onError"
                    @cameras="onCameras"
                    @camera-change="onCameraChange"
                />
                <div
                    style="border:1px solid white;
    width:88%;
    margin:25px auto;"
                ></div>
                <p class="mb-15 pl-15" style="font-size:28px;">
                    카메라 정면을 봐주시고 <br />우측의 결제버튼을 클릭해주세요.
                </p>
                <v-spacer></v-spacer>
            </div>
            <div class="col-3" style="padding-top: 200px;">
                <p class="introduceMessage" style="padding-top:20px;">
                    결제를 원하시면 <br />버튼을 눌러주세요.
                </p>
                <v-img
                    v-if="!pay_c"
                    class="wonImage"
                    @mouseover="domouseover_pay"
                    @click="checkPayment"
                    :src="require('../assets/images/click(w).png')"
                ></v-img>
                <v-img
                    v-else
                    class="wonImage"
                    @mouseout="domouseout_pay"
                    @click="checkPayment"
                    :src="require('../assets/images/click.png')"
                ></v-img>
            </div>
        </v-row>
        <v-spacer></v-spacer>
    </v-container>
</template>

<script>
import { WebCam } from 'vue-web-cam';
import swal from 'sweetalert';

export default {
    name: 'App',
    components: {
        'vue-web-cam': WebCam,
    },
    data() {
        return {
            img: null,
            camera: null,
            deviceId: null,
            devices: [],
            total: '',
            won_c: false,
            pay_c: false,
        };
    },
    computed: {
        device: function() {
            return this.devices.find((n) => n.deviceId === this.deviceId);
        },
    },
    watch: {
        camera: function(id) {
            this.deviceId = id;
        },
        devices: function() {
            // Once we have a list select the first one
            const [first, ...tail] = this.devices; // eslint-disable-line no-unused-vars
            if (first) {
                this.camera = first.deviceId;
                this.deviceId = first.deviceId;
            }
        },
    },
    methods: {
        domouseover_won() {
            this.won_c = true;
        },
        domouseout_won() {
            this.won_c = false;
        },
        domouseover_pay() {
            this.pay_c = true;
        },
        domouseout_pay() {
            this.pay_c = false;
        },
        checkTotal() {
            this.won_c = !this.won_c;
            if (this.won_c == false) {
                console.log('금액확인');
                this.total = '￦ 1,000,000';
            } else this.total = '';
        },
        checkPayment() {
            this.pay_c = !this.pay_c;
            if (this.pay_c == false) {
                swal('결제를 진행합니다', {
                    icon: 'success',
                });
            }
        },
        onCapture() {
            this.img = this.$refs.webcam.capture();
        },
        onStarted(stream) {
            console.log('On Started Event', stream);
        },
        onStopped(stream) {
            console.log('On Stopped Event', stream);
        },
        onStop() {
            this.$refs.webcam.stop();
        },
        onStart() {
            this.$refs.webcam.start();
        },
        onError(error) {
            console.log('On Error Event', error);
        },
        onCameras(cameras) {
            this.devices = cameras;
            console.log('On Cameras Event', cameras);
        },
        onCameraChange(deviceId) {
            this.deviceId = deviceId;
            this.camera = deviceId;
            console.log('On Camera Change Event', deviceId);
        },
    },
};
</script>
<style scoped>
@import '../assets/css/cam.css';
@import '../assets/css/camPayment.css';
</style>
