<template>
        <v-container class="col-6 centerContent">
            <h1 class="centerText">고객 등록</h1>
            <div class="col-6 centerContent">
                    <v-img
                    lazy-src="https://picsum.photos/id/11/10/6"
                    height="300"
                    src="https://picsum.photos/id/11/500/300"
                    class="profileImg col-4 centerContent"
                    ></v-img>
                    <v-file-input
                    accept="image/*"
                    label="사진 변경"
                    dark
                    >
                    </v-file-input>
                    <v-row style="margin:0; padding:0;">
                        <v-text-field
                        label="name"
                        type="string"
                        dark></v-text-field> 
                        <v-spacer></v-spacer>
                        <v-text-field
                        label="나이"
                        type="number"
                        dark></v-text-field>                       
                    </v-row>
                    <v-text-field
                    label="관심분야"
                    type="string"
                    dark></v-text-field>
                    <v-text-field
                    label="요구사항"
                    type="string"
                    dark></v-text-field>
                    <v-row style="margin:0; padding:0;">
                        <v-spacer></v-spacer>
                            <v-btn
                            elevation="2"
                            class="resetBtn"
                            >초기화</v-btn>

                            <v-btn
                            elevation="2" 
                            class="registBtn"
                            >등록</v-btn>
                    </v-row>
            </div>
            

        </v-container>
    
    
</template>

<script>
export default {
    
}
</script>

<style scoped>
@import '../assets/css/customerRegister.css';

</style>