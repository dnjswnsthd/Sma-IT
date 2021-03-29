import axios from 'axios';
// axios 객체 생성
export default axios.create({
    
    baseURL: 'https://j4d102.p.ssafy.io', // baseUrl
    headers: {
        'Content-type': 'application/json',
    },
});
 