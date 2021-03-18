<template>
        <v-container class="col-6 centerContent">
            <p class="centerText registerTitle">고객 등록</p>
            <div class="col-6 centerContent">
                    <v-img
                    
                    height="300"
                    src="../assets/images/profile.png"
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
                    <v-textarea
                    outlined
                    label="요구사항"
                    type="string"
                    dark></v-textarea>
                    <v-row style="margin:0; padding:0;">
                        <v-spacer></v-spacer>
                            <button
                            
                            class="resetBtn"
                            >초기화</button>

                            <button
                            
                            class="registBtn"
                            >등록</button>
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