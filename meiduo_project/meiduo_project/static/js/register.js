var vm = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    data: {
        // v-model
        username: '',
        password1: '',
        password2: '',
        phone_num: '',
        pic_verification_code: '',
        message_code: '',
        allow: '',

        // v-show
        error_name: false,
        error_password1: false,
        error_password2: false,
        error_phone_num: false,
        error_pic_code: false,
        error_message_code: false,
        error_allow: false,

        // 变量
        error_name_message: '',
        error_mobile_message: '',



// 请输入8-20位的密码(仅能输入'@' '.' '_'特殊字符)
    },

    // 事件
    methods: {
        // 检查username
        check_username(){
            // 正则匹配格式/^ .... $/
            let re = /^[\w]{5,20}$/
            let re2 = /^[\d]{5,20}$/
            if (re.test(this.username)){

                this.error_name = false
                if (re2.test(this.username)){
                    
                    this.error_name_message = '用户名不能全为数字!'
                    this.error_name = true
                }
                
            }else{
                
                this.error_name_message = '请输入5-20个字符的用户名(不能使用特殊字符)'
                this.error_name = true
            }
        },
        check_password1(){
            let re = /^[0-9a-zA-z@._]{8,20}$/
            if (re.test(this.password1)){
                this.error_password1 = false
            }else{
                this.error_password1 = true
            }
        },
        check_password2(){
            if (this.password1 != this.password2){
                this.error_password2 = true
            }else{
                this.error_password2 = false
            }
        },
        check_phone_num(){

        },
        check_pic_verification_code(){

        },
        check_message_code(){

        },
        check_allow(){
            if (this.allow){
                this.error_allow = false
            }else{
                this.error_allow = true
            }
        },
        // 监听表单提交事件
		on_submit(){
			this.check_username();
			this.check_password();
			this.check_password2();
			this.check_mobile();
			this.check_allow();

			if(this.error_name == true || this.error_password == true || this.error_password2 == true
				|| this.error_mobile == true || this.error_allow == true) {
                // 禁用表单的提交
                
				window.event.returnValue = false;
            }
		},

    },
    


})