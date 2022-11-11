var vm = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    data: {
        // 空值判断开关
        isnull_username: true,
        isnull_password1: true,
        isnull_phone: true,

        // v-model
        username: '',
        password1: '',
        password2: '',
        phone_num: '',
        pic_verification_code: '',
        message_code: '',
        allow: false,

        // v-show
        error_name_show: false,
        error_password1_show: false,
        error_password2_show: false,
        error_phone_show: false,
        error_pic_code_show: false,
        error_message_code_show: false,
        error_allow_show: false,
        

        // 变量
        error_name_message: '',
        error_phone_message: '',
        register_errmsg: '',
        error_allow_message: '',
        



// 请输入8-20位的密码(仅能输入'@' '.' '_'特殊字符)
    },

    // 事件
    methods: {
        // 检查username
        check_username(){
            // 正则匹配格式/^ .... $/
            // 匹配文本[a-zA-Z_汉字]
            let re = /^[a-zA-Z0-9]{5,20}$/
            // 匹配纯数字
            let re2 = /^[\d]{5,20}$/
            // 匹配空输入
            let re3 = /^$/
            
            // 1) 判断是否输入空值
            if (re3.test(this.username)){ // 是空值
                
                // 输入空值不显示错误信息
                this.error_name = false
                this.isnull_username = true
                
            }else{
                // 2) 判断是否全数字
                if (re2.test(this.username)){ // 是全数字
                    this.error_name_message = '用户名不能全为数字!'
                    this.error_name_show = true
                }else{
                    // 3) 判断是否符合正则
                    if (re.test(this.username)){ // 符合条件
                        this.error_name_show = false
                        // 关闭空值
                        this.isnull_username = false
                    }else{ 
                        this.error_name_message = '请输入5-20个英文字母,数字的组合字符的用户名'
                        this.error_name_show = true
                    }
                }
            }
            
            
            
        },
        check_password1(){
            let re = /^[0-9a-zA-z@._]{8,20}$/
            let re2 = /^$/
            
            if (re2.test(this.password1)){
                this.error_password1_show = false
                this.isnull_password1 = true
            }else{
                if (re.test(this.password1)){
                    this.error_password1_show = false
                    this.isnull_password1 = false
                }else{
                    this.error_password1_show = true
                }
            }
            
        },
        check_password2(){
                if (this.password1 != this.password2){
                    this.error_password2_show = true
                }else{
                    this.error_password2_show = false
                }
            
        },
        check_phone_num(){
            let re = /^1[3-9]\d{9}$/
            let re2 = /^$/
            if (re2.test(this.phone_num)){
                this.error_phone_show = false
                this.isnull_phone = true
            }else{
                if (re.test(this.phone_num)){
                    this.error_phone_show = false
                    this.isnull_phone = false
                }else{
                    this.error_phone_message = '手机号码格式错误'
                    this.error_phone_show = true
                }
            }

        },
        check_pic_verification_code(){

        },
        check_message_code(){

        },
        check_allow(){
            if (this.allow){
                this.error_allow_show = false
                return true
            }else{
                this.error_allow_message = '请勾选用户协议'
                this.error_allow_show = true
                window.event.returnValue = false;
                return false
            }

        },
        // 清空表单
        reset_form(){
            
        },

        // 监听表单提交事件
        on_submit(){
            this.check_username();
            this.check_password1();
            this.check_password2();
			this.check_phone_num();
			// 先检查allow是否同意
            if(this.check_allow()){ // 再检查参数填写完整性
                // 填入空值禁用提交
                if(this.isnull_username == true || this.isnull_password1 == true || this.isnull_phone == true){
                    this.error_allow_message = '注册信息未填写完整!'
                    this.error_allow_show = true

                    // 定时器实现'注册信息未填写完整!'延迟3秒自动消失
                    // setTieout在vue内使用要用箭头函数重新指向vue对象, 默认是window对象
                    setTimeout(()=>{
                        this.error_allow_message = ''
                        this.error_allow_show = false
                    },3000) 
                    window.event.returnValue = false;
                    
                    
                }
            }

            

			if(this.error_name_show == true || this.error_password1_show == true || this.error_password2_show == true
				|| this.error_phone_show == true || this.error_allow_show == true) {
                // 禁用表单的提交
                
				window.event.returnValue = false;
                
            }
            
		},

    },
    


})