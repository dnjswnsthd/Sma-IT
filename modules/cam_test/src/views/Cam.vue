<template>
  <v-container>
    <v-row>
      <div class="col-6"></div>
      <div class="col-6 cambox">
        <!-- <h2>Current Camera</h2>
                <code v-if="device">{{ device.label }}</code> -->
        <vue-web-cam
          ref="webcam"
          :device-id="deviceId"
          style="margin-top: 90px; border-radius: 10%"
          width="100%"
          height="520px"
          @started="onStarted"
          @stopped="onStopped"
          @error="onError"
          @cameras="onCameras"
          @camera-change="onCameraChange"
        />
        <hr style="margin-top: 15px" />
        <h1
          style="
            text-align: center;
            color: white;
            margin-top: 15px;
            margin-bottom: 70px;
            display: block;
          "
        >
          얼굴을 가이드라인에 맞춰주시고 <br />인식이 완료될때까지 잠시
          기다려주세요
        </h1>
        <br /><br />
        <!-- <div class="row">
                    <div class="col-md-12">
                        <select v-model="camera">
                            <option>-- Select Device --</option>
                            <option
                                v-for="device in devices"
                                :key="device.deviceId"
                                :value="device.deviceId"
                                >{{ device.label }}</option
                            >
                        </select>
                    </div>
                    <div class="col-md-12">
                        <button type="button" class="btn btn-primary" @click="onCapture">
                            Capture Photo
                        </button>
                        <button type="button" class="btn btn-danger" @click="onStop">
                            Stop Camera
                        </button>
                        <button type="button" class="btn btn-success" @click="onStart">
                            Start Camera
                        </button>
                    </div>
                </div> -->
      </div>
      <!-- <div class="col-md-6">
        <h2>Captured Image</h2>
        <figure class="figure">
          <img :src="img" class="img-responsive" />
        </figure>
      </div> -->
    </v-row>
  </v-container>
</template>

<script>
import { WebCam } from "vue-web-cam";
export default {
  name: "App",
  components: {
    "vue-web-cam": WebCam,
  },
  data() {
    return {
      img: null,
      camera: null,
      deviceId: null,
      devices: [],
    };
  },
  computed: {
    device: function () {
      return this.devices.find((n) => n.deviceId === this.deviceId);
    },
  },
  watch: {
    camera: function (id) {
      this.deviceId = id;
    },
    devices: function () {
      // Once we have a list select the first one
      const [first, ...tail] = this.devices; // eslint-disable-line no-unused-vars
      if (first) {
        this.camera = first.deviceId;
        this.deviceId = first.deviceId;
      }
    },
  },
  methods: {
    onCapture() {
      this.img = this.$refs.webcam.capture();
    },
    onStarted(stream) {
      console.log("On Started Event", stream);
    },
    onStopped(stream) {
      console.log("On Stopped Event", stream);
    },
    onStop() {
      this.$refs.webcam.stop();
    },
    onStart() {
      this.$refs.webcam.start();
    },
    onError(error) {
      console.log("On Error Event", error);
    },
    onCameras(cameras) {
      this.devices = cameras;
      console.log("On Cameras Event", cameras);
    },
    onCameraChange(deviceId) {
      this.deviceId = deviceId;
      this.camera = deviceId;
      console.log("On Camera Change Event", deviceId);
    },
  },
};
</script>
<style scoped>
.cambox {
  background-image: url("../assets/images/frame2.png");
  background-position: center center;
  background-size: 100% 100%;
  padding-top: 10px;
  padding-left: 100px;
  padding-right: 100px;
}
</style>
