let vm = new Vue({
    el: '#app',
    // 修改Vue变量的读取语法
    delimiters: ['[[', ']]'],
    data: {
        username: '',
        password: '',

        // 错误信息
        error_username_message: '',

        // v-show
        error_username: false,
        error_password: false,
        remembered: false,
    },
    methods: {
        // 检查账号
        check_username(){
            this.error_username = false
            if(this.username == ''){
                this.error_username = true
            }
            // 校验是否注册
            if(this.error_username == false){
                let url1 = '../isReg/' + this.username + "/count/"
                // ---------------校验用户名-----------
                axios.get(url1,{
                    responseType: 'json'
                }).then((response) => { // 成功执行
                    if(response.data.username_count == 0 && response.data.mobile_count == 0){
                        this.error_username_message = '该用户未注册, 请先注册!'
                        this.error_username = true
                    }
                }).catch(() => { // 失败执行
                    console.log(error.response)
                })
            }
            
        },
		// 检查密码
        check_password(){
            this.error_password = false
            if(this.password == ''){
                this.error_password = true
            }

        },
        // 表单提交
        on_submit(){
            this.check_username();
            this.check_password();

            if (this.error_username == true || this.error_password == true) {
                // 不满足登录条件：禁用表单
				window.event.returnValue = false
            }
        },
        // qq登录
        qq_login(){
            let next = get_query_string('next') || '/';
            let url = '/qq/login/?next=' + next;
            axios.get(url, {
                responseType: 'json'
            })
                .then(response => {
                    location.href = response.data.login_url;
                })
                .catch(error => {
                    console.log(error.response);
                })
        }
    }
});