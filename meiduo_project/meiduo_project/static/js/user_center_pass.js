let vm = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    data: {
        username: getCookie('username'),
        old_password: '',
        new_password: '',
        new_password2: '',
        error_old_password: false,
        error_new_password: false,
        error_new_password2: false,

        error_new_password_message: '',
        // v-bind显示密码
        type_old_password: 'password',
        type_new_password: 'password',
        type_new_password2: 'password',
        // 变量
        show_old_password_msg: '显示',
        show_new_password_msg: '显示',
        show_new_password2_msg: '显示',

        // 显示信号
        show_old_password_flag: false,
        show_new_password_flag: false,
        show_new_password2_flag: false,
    },
    methods: {
        // 检查旧密码
        check_old_password(){
        	let re = /^.{8,20}$/;
            if (re.test(this.old_password)) {
                this.error_old_password = false;
            } else {
                this.error_old_password = true;
            }
        },
        // 检查新密码
        check_new_password(){
            // 新旧密码不能一直
            if (this.old_password == this.new_password) {
                this.error_new_password = true;
                this.error_new_password_message = '新密码不能和旧密码一致';
                return false
            } else {
                this.error_new_password = false;
            }
            let re = /^.{8,20}$/
            let re2 = /^$/
            let re3 = /.*[a-zA-Z]+.*/ // 包含字母
            let re4 = /.*\d+.*/ // 包含数字
            if (re2.test(this.new_password)) {
                this.error_new_password = false
            } else {
                if (re.test(this.new_password)) { // 符合正则
                    this.error_new_password = false
                    // 不符合强度
                    if (!(re3.test(this.new_password) && re4.test(this.new_password))) { // 密码强度不符合
                        this.error_new_password_message = '密码强度过低!至少包含字母和数字组合'
                        this.error_new_password = true
                    }

                } else { // 不符合正则
                    this.error_new_password_message = '请输入8-20位的密码'
                    this.error_new_password = true

                }
            }
        },
        // 检查确认密码
        check_new_password2(){
            if (this.new_password != this.new_password2) {
                this.error_new_password2 = true;
            } else {
                this.error_new_password2 = false;
            }
        },
        // 提交修改密码
        on_submit(){
            this.check_old_password();
            this.check_new_password();
            this.check_new_password2();

            if (this.error_old_password==true || this.error_new_password==true || this.error_new_password2==true) {
                // 不满足修改密码条件：禁用表单
				window.event.returnValue = false
            }
        },
        // 显示密码
        show_old_password(){
            if(this.show_old_password_flag == true){
                this.type_old_password = 'password'
                this.show_old_password_msg = '显示'
                this.show_old_password_flag = false
            }else{
                this.type_old_password = 'text'
                this.show_old_password_msg = '隐藏'
                this.show_old_password_flag = true
            }
            
        },
        show_new_password(){
            if(this.show_new_password_flag == true){
                this.type_new_password = 'password'
                this.show_new_password_msg = '显示'
                this.show_new_password_flag = false
            }else{
                this.type_new_password = 'text'
                this.show_new_password_msg = '隐藏'
                this.show_new_password_flag = true
            }
            
        },
        show_new_password2(){
            if(this.show_new_password2_flag == true){
                this.type_new_password2 = 'password'
                this.show_new_password2_msg = '显示'
                this.show_new_password2_flag = false
            }else{
                this.type_new_password2 = 'text'
                this.show_new_password2_msg = '隐藏'
                this.show_new_password2_flag = true
            }
            
        },
    }
});