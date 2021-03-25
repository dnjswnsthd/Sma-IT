<template>
    <v-container>
        <v-row class="wrapBox">
            <div class="col-6">
                <p class="introduceMessage" style="padding-top:20px;">방문을 진심으로<br />환영합니다.</p>
                <div class="productBox">
                    <div class="newProducts">
                        <p>New 상품!</p>
                        <v-row class="newRow">
                            <v-item v-for="n in 3"
                            :key="n"
                            style="margin:0 16px;"
                            >
                                <div class="itemBox">
                               
                                </div>
                            </v-item>
                        </v-row>
                    </div>
                    <div class="saleProducts">
                        <p>Sale 상품!</p>
                        <v-row class="saleRow">
                            <v-item v-for="n in 3"
                            :key="n"
                            style="margin:0 16px;"
                            >
                                <div class="itemBox"></div>
                            </v-item>
                        </v-row>
                    </div>
                </div>
            </div>
            <div class="col-6 cambox">
                <!-- <vue-web-cam
                    ref="webcam"
                    :device-id="deviceId"
                    style="margin-top: 70px; "
                    width="100%"
                    height="580px"
                    @stopped="onStopped"
                    @error="onError"
                    @cameras="onCameras"
                    @camera-change="onCameraChange"
                /> -->
                
                <div class="camInnerBox">
                    <canvas ref="canvas" id="emo_canvas" width="650px" height="650px" class="canvasBox"></canvas>
                    <video ref="video" id="video" height="650px" playsinline muted autoplay class="videoBox"></video>
                </div>
                <div class="divider"></div>
                <v-row>
                   <p class="guideMessage" style="padding-left:80px;">얼굴을 가이드라인에 맞춰주시고 <br />클릭 버튼을 눌러주세요!</p> 
                   <button @click="goCapture" style="color: gold; font-size:40px;">Click</button>
                </v-row>
                
            </div>
        </v-row>
        <v-btn @click="goCamPayment">결제화면보기</v-btn>
        
    </v-container>
</template>

<script>
// import { WebCam } from 'vue-web-cam';
import http from '../api/axios';
import Axios from 'axios';

export default {
    name: 'App',
    components: {
        // 'vue-web-cam': WebCam,
    },
    data() {
        return {
            img: null,
            camera: null,
            deviceId: null,
            devices: [],
            video: {},
      canvas: {},
      captures: [],
      testTimer: '',
      decodeUrl:'',
      imgUrl:'',
      formValues:{},
        };
    },
    computed: {
        device: function() {
            return this.devices.find((n) => n.deviceId === this.deviceId);
        },
    },
    mounted() {
  //Start the PC front camera and display real-time video on the video tag
    this.video = this.$refs.video
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      navigator.mediaDevices.getUserMedia({audio: false, video: true})
      .then(stream => {
        this.video.srcObject = stream
        this.video.play()
      })
    }

    console.log(this.$refs.canvas);
    // console.log(this.$refs.canvas)

    this.canvas = this.$refs.canvas 
    // this.testTimer = this.goCapture();
    // this.testTimer = function() {
    //   // console.log(this.$refs.canvas)
    //   let context = this.canvas.getContext("2d").drawImage(this.video, 0, 0, 400, 240);
    //   console.log("context : " + context);
    //   this.captures.push(this.canvas.toDataURL("image/png")) //Store the captured image in the "captures" array
    //   let subscriptionKey = "c2ade783cde74c478a3f5ec193cf6b3f";
    //   let uriBase = "https://koreacentral.api.cognitive.microsoft.com/face/v1.0/detect/";
    // //   https://smait.cognitiveservices.azure.com/
    //   let params = {
    //     "returnFaceId": "false",
    //     "returnFaceLandmarks": "true",
    //     "returnFaceAttributes":
    //       "emotion"
    //   };
    //   console.log(params);
    // //   //Convert the format of the image added at the end of the array and assign it to the imgURL format
    //   const imgURL = this.makeblob(this.captures[this.captures.length - 1])
    //   //Send imgURL image to Face API
    //   Axios.post(
    //     uriBase + "?returnFaceId=true&returnFaceLandmarks=false&returnFaceAttributes=age,emotion",
    //     imgURL,
    //     {
    //       headers: {
    //         "Content-Type": "application/octet-stream",
    //         "Ocp-Apim-Subscription-Key": subscriptionKey,
    //       }
    //     },
        
    //   )
    //   .then(response => {
    //     console.log(response.data[0].faceAttributes.emotion)

    //   })
    //   .catch(error => {
    //     console.log(error.response);
    //   });
    // };
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
        goCapture(){
            // console.log(this.$refs.canvas)
            
      let context = this.canvas.getContext("2d").drawImage(this.video, 0, 0, 728, 650);
      console.log("context : " + context);
      this.captures.push(this.canvas.toDataURL("image/png")) //Store the captured image in the "captures" array
    //   console.log(this.captures);
    //   this.decodeUrl = window.atob(this.captures);
    //   console.log('decode : ' + this.decodeUrl);
      
      // Define the string
 
// Decode the String
// var decodedString = atob(string);

// console.log(decodedString); // Outputs: "Hello World!"


      let subscriptionKey = "c2ade783cde74c478a3f5ec193cf6b3f";
      let uriBase = "https://koreacentral.api.cognitive.microsoft.com/face/v1.0/detect/";
    //   https://smait.cognitiveservices.azure.com/
      let params = {
        "returnFaceId": "false",
        "returnFaceLandmarks": "true",
        "returnFaceAttributes":
          "emotion"
      };
      console.log(params);
    //   //Convert the format of the image added at the end of the array and assign it to the imgURL format
      const file = this.makeblob(this.captures[this.captures.length - 1])
      console.log('imgURL : ' + file);

    //   const fileName = 'canvas_img_'+new Date().getMilliseconds()+'.png';
      let formData = new FormData();
      formData.append('file', file);
      console.log(file);
    //   console.log(formData.values());
    //   for(var value of formData.values()){
    //       this.formValues = value;
    //   }
    // let captureImg = this.formValues;
    // //   console.log(this.formValues);
    //console.log(formData.toDataURL)
        http.post(`/face/`,formData).then((response)=>{
            console.log(response.data);
            alert('승공');
        }).catch(()=>{
            alert('실패');
        })
        
      //Send imgURL image to Face API
      Axios.post(
        uriBase + "?returnFaceId=true&returnFaceLandmarks=false&returnFaceAttributes=age,emotion",
        file,
        {
          headers: {
            "Content-Type": "application/octet-stream",
            "Ocp-Apim-Subscription-Key": subscriptionKey,
          }
        },
        
      )
      .then(response => {
        console.log(response.data[0].faceAttributes.emotion)
        
      })
      .catch(error => {
        console.log(error.response);
      });
        },
        makeblob: function (dataURL) {
            let BASE64_MARKER = ';base64,';
            if (dataURL.indexOf(BASE64_MARKER) == -1) {
                let parts = dataURL.split(',');
                let contentType = parts[0].split(':')[1];
                let raw = decodeURIComponent(parts[1]);
                return new File([raw], {type: contentType});
            }
            let parts = dataURL.split(BASE64_MARKER);
            let fileName = 'ssibalimage';
            let contentType = parts[0].split(':')[1];
            let raw = window.atob(parts[1]);
            let rawLength = raw.length;
            let uInt8Array = new Uint8Array(rawLength);
            for (let i = 0; i < rawLength; ++i) {
                uInt8Array[i] = raw.charCodeAt(i);
            }
            return new File([uInt8Array],fileName, {type: contentType})
        },

        goCamPayment(){
            this.$router.push({name:'CamPayment'});
        }
    },
};
</script>
<style scoped>
@import '../assets/css/cam.css';
.camInnerBox{
    height:65%;
    position:relative;
}
.canvasBox{
    display:block;
    position:absolute;
    left:50%; top:0;
    margin-top:100px;
    margin-left:-200px;
    z-index:-1;
}
.videoBox{
    display:block;
    width: calc(100% - 140px);
    margin: 0 auto;
}
.clickBtn{
    position:absolute;
    right:10%;bottom:0%;
}
</style>
