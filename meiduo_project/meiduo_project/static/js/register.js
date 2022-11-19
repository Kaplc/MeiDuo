var vm = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    data: {

        // v-model
        username: '',
        password1: '',
        password2: '',
        phone_num: '',
        img_code: '',
        message_code: '',
        allow: false,

        // v-show
        error_name_show: false,
        error_password1_show: false,
        error_password2_show: false,
        error_phone_show: false,
        error_image_code_show: false,
        error_message_code_show: false,
        error_allow_show: false,
        error_register_show: false,
        

        // 错误信息变量
        error_name_message: '',
        error_password1_message: '',
        error_phone_message: '',
        error_image_code_message: '',
        error_message_code_tip: '',
        register_errmsg: '',
        error_allow_message: '',
        error_register: '',

        // uuid
        uuid: null,
        image_code_url: null,

        // 提示信息
        message_code_tip: '获取短信验证码',

        // 信号
        sending_flag: true,
        



// 请输入8-20位的密码(仅能输入'@' '.' '_'特殊字符)
    },

    // 事件
    methods: {
        // 检查username规则
        check_username_rule(){
            // 重置错误提示
            this.error_name_show = false
            // 正则匹配格式/^ .... $/
            // 匹配文本[a-zA-Z_汉字]
            let re = /^[a-zA-Z0-9_]{5,20}$/
            // 匹配纯数字
            let re2 = /^[\d]{5,20}$/
            // 匹配空输入
            let re3 = /^$/
            
            // 1) 判断是否输入空值
            if (re3.test(this.username)){ // 是空值
                
                // 输入空值不显示错误信息
                this.error_name_message = ''
                this.error_name_show = true
            }
            // 2) 判断是否全数字
            if (this.error_name_show == false){ // 判断上一条if是否错误
                if(re2.test(this.username)){
                    this.error_name_message = '用户名不能全为数字!'
                    this.error_name_show = true
                }  
            }
            // 判断是否符合正则表达式
            if(this.error_name_show == false){
                if(!re.test(this.username)){ // 不符合正则
                    this.error_name_message = '请输入5-20个英文字母,数字的组合字符的用户名'
                    this.error_name_show = true
                }
            }
            // 符合正则
            if(this.error_name_show == false){
                // 检查用户名重复
                this.check_username_isright()
            }
 
        },
        // 校验是否username重复
        check_username_isright(){
            // 判断用户名是否重复注册
            if(this.error_name_show == false){
                let url = '../usernames/' + this.username + '/count/'
                // get(请求地址, 返回的数据类型)
                axios.get(url,{
                    responseType: 'json'
                }).then((response) => { // 成功执行
                    if(response.data.count == 1){
                        this.error_name_message = '用户名已被使用'
                        this.error_name_show = true
                        setTimeout(() => {
                            this.error_name_message = ''
                            this.error_name_show = false
                        }, 2000)
                    }else{
                        
                        this.error_name_show = false
                    }
                }).catch(() => { // 失败执行
                    console.log(error.response)
                })
            }
        },
        // 校验密码
        check_password1(){
            // 重置
            this.error_password1_message = ''
            this.error_password1_show = false

            let re = /^.{8,20}$/
            let re2 = /^$/
            let re3 = /.*[a-zA-Z]+.*/ // 包含字母
            let re4 = /.*\d+.*/ // 包含数字
            if (re2.test(this.password1)){
                this.error_password1_show = false
            }else{
                if (re.test(this.password1)){ // 符合正则
                    this.error_password1_show = false
                    if(!(re3.test(this.password1) && re4.test(this.password1))){ // 密码强度不符合
                        this.error_password1_message = '密码强度过低!至少包含字母和数字组合'
                        this.error_password1_show = true
                    }
                    
                }else{ // 不符合正则
                    this.error_password1_message = '请输入8-20位的密码'
                    this.error_password1_show = true
                    
                }
            }
            
        },
        // 再次确认密码
        check_password2(){
                if (this.password1 != this.password2){
                    this.error_password2_show = true
                }else{
                    this.error_password2_show = false
                }
            
        },
        check_phone_num(){

        },
        // 生成图形验证码
        generate_image_code(){
            // 调用common.js内的函数生成uuid
            this.uuid = generateUUID() 
            // 拼接图形验证码请求地址
            this.image_code_url = "../verify/get_image_codes/" + this.uuid + "/" 

        },
        // 发送短信验证码
        send_message_code(){
            // 校验手机号格式
            let re = /^1[3-9]\d{9}$/
            let re2 = /^$/
            // 重置错误提示
            this.error_phone_show = false
            // 校验是否填写
            if (re2.test(this.phone_num)){
                this.error_phone_message = '请填写手机号'
                this.error_phone_show = true
            }
            // 校验手机号格式
            if(this.error_phone_show == false){
                if (!re.test(this.phone_num)){ // 格式错误
                    this.error_phone_message = '手机号码格式错误'
                    this.error_phone_show = true
                }    
            }
            // -------------------------------------------------
            // 校验手机号是否重复
            if(this.error_phone_show == false){
                let url = "../mobiles/" + this.phone_num + "/count/"
                    axios.get(url, {
                        responseType: 'json'
                    }).then((response) => { 
                        if(response.data.count == 1){ // 手机号重复
                            this.error_phone_message = "该手机号已注册, 请登录"
                            this.error_phone_show = true

                        }else{ // 手机号未注册

                            // ---------------------------------------
                            // 校验图片验证码是否填写
                            this.error_image_code_show = false // 重置错误参数
                            if(this.img_code == ''){
                                this.error_image_code_message = '请填写图形验证码'
                                this.error_image_code_show = true
                            }

                            // 校验图形验证码正确性和发送短信
                            if(this.error_image_code_show == false){
                                // 拼接验证图形验证码,发送短信验证码请求地址
                                let url = "../verify/send_message_code/" + this.phone_num + "/" + this.img_code + "/" + this.uuid + "/"
                                
                                // 阻止重复点击
                                if(this.sending_flag == false){
                                    this.error_message_code_tip = '请求过于频繁'
                                    return
                                }

                                axios.get(url, {
                                    responseType: 'json'
                                }).then((response) => { // 请求成功
                                    if(response.data.code == "0"){
                                        // 验证成功发送短信验证码
                                        // alert('短信验证码发送成功')
                                        this.sending_flag = false

                                        // 渲染倒计时60秒
                                        let time = 60
                                        cound_down = setInterval(() => {
                                            this.message_code_tip = '重新发送' + time + "秒"
                                            time -= 1
                                            if(time <= -1){
                                                this.message_code_tip = '获取短信验证码'
                                                this.sending_flag = true
                                                clearInterval(cound_down)
                                            }
                                        }, 1000)
                                        
                                    }else{
                                        // 刷新验证码, 显示错误
                                        this.generate_image_code()
                                        this.error_image_code_message = '图形验证码错误'
                                        this.error_image_code_show = true
                                        
                                    }
                                }).catch((response) => {
                                    // 刷新验证码, 显示错误
                                    this.generate_image_code()
                                    this.error_image_code_message = '图形验证码错误'
                                    this.error_image_code_show = true
                                    console.log(response)
                                })
                            }
                            
                        }
                    }).catch((response) => {
                        console.log(response)
                    })
            }          

        },

        // 校验是否同意协议
        check_allow(){
            if (this.allow){
                this.error_allow_show = false
                return true
            }else{
                this.error_allow_message = '请勾选用户协议'
                this.error_allow_show = true
                return false
            }

        },
        // 监听表单提交事件
        on_submit(){
            this.check_username_rule();
            this.check_password1();
            this.check_password2();
			this.check_phone_num();
            if(this.check_allow()){// 先判断协议是否同意
                // 填入空值禁用提交
                if(this.username == '' || this.password1 == '' || this.password2 == '' || this.phone_num == '' || this.img_code == '' || this.message_code == ''){
                    this.error_register = '注册信息未正确填写!'
                    this.error_register_show = true

                    // 定时器实现'注册信息未填写完整!'延迟3秒自动消失
                    // setTieout在vue内使用要用箭头函数重新指向vue对象, 默认是window对象
                    setTimeout(()=>{
                        this.error_register = ''
                        this.error_register_show = false
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
    // 生命周期事件
    mounted() {
        // 刷新图形验证码
        
        this.generate_image_code()
            
       
    },


})