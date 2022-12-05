let vm = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    data: {
        username: getCookie('username'),
        mobile: mobile,
        email: email,
        email_active: email_active,

        set_email: false,
        error_email: false,
        send_flag: true,

        send_email_btn_disabled: false,
        send_email_tip: '验证',
        update_email_botton_tip: '确认修改',
        verify_message: '已验证',
        histories: [],
    },
    mounted() {
        // 邮箱是否激活：将Python的bool数据转成JS的bool数据
        this.email_active = (this.email_active == 'True') ? true : false;
        // 是否在设置邮箱
        this.set_email = (this.email == '') ? true : false;

        // 请求浏览历史记录
        this.browse_histories();
    },
    methods: {
        // 加入购物车
        add_carts(){
            let url = '/carts/';
            axios.post(url, {
                sku_id: parseInt(this.sku_id),
                count: this.sku_count
            }, {
                headers: {
                    'X-CSRFToken':getCookie('csrftoken')
                },
                responseType: 'json',
                withCredentials: true
            })
                .then(response => {
                    if (response.data.code == '0') {
                        alert('添加购物车成功');
                        this.cart_total_count += this.sku_count;
                    } else { // 参数错误
                        alert(response.data.errmsg);
                    }
                })
                .catch(error => {
                    console.log(error.response);
                })
        },
        // 检查email格式
        check_email() {
            let re = /^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$/;
            if (re.test(this.email)) {
                this.error_email = false;
            } else {
                this.error_email = true;
            }
        },
        // 取消保存
        cancel_email() {
            this.email = '';
            this.error_email = false;
        },
        // 保存email
        save_email() {
            // 检查email格式
            this.check_email();
            if (this.send_flag == false) {
                return false
            }
            if (this.error_email == false) {
                this.send_flag = false
                let url = '/emails/';
                axios.put(url, {
                    email: this.email
                }, {
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    responseType: 'json'
                })
                    .then(response => {
                        if (response.data.code == '0') {
                            this.set_email = false;
                            this.send_email_btn_disabled = true;
                            
                            let time = 60
                            cound_down = setInterval(() => {
                                this.send_email_tip = '已发送验证邮件' + time + "秒重试"
                                time -= 1
                                if (time <= -1) {
                                    this.send_email_tip = '发送验证邮件'
                                    this.send_flag = true
                                    clearInterval(cound_down)
                                }
                            }, 1000)
                        } else if (response.data.code == '4101') {
                            location.href = '/login/?next=/info/';
                        } else {
                            this.send_flag = true
                            alert(response.data.errmsg);
                        }
                    })
                    .catch(error => {
                        this.send_flag = true
                        console.log(error.response);
                    });
            }
        },
        // 更新邮箱
        update_email() {
            // 检查email格式
            this.check_email();
            if (this.send_flag == false) {
                return false
            }
            if (this.error_email == false) {
                this.send_flag = false
                let url = '/emails/';
                axios.put(url, {
                    email: this.email
                }, {
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    responseType: 'json'
                })
                    .then(response => {
                        if (response.data.code == '0') {
                            this.set_email = false;
                            this.send_email_btn_disabled = true;
                            this.verify_message = '未验证'
                            let time = 60
                            cound_down = setInterval(() => {
                                this.update_email_botton_tip = '已发送验证邮件' + time + "秒重试"
                                time -= 1
                                if (time <= -1) {
                                    this.update_email_botton_tip = '发送验证邮件'
                                    this.send_flag = true
                                    clearInterval(cound_down)
                                }
                            }, 1000)
                        } else if (response.data.code == '4101') {
                            location.href = '/login/?next=/info/';
                        } else {
                            this.send_flag = true
                            alert(response.data.errmsg);
                        }
                    })
                    .catch(error => {
                        this.send_flag = true
                        console.log(error.response);
                    });
            }
        },
        // 请求浏览历史记录
        browse_histories() {
            let url = '/browse_histories/';
            axios.get(url, {
                responseType: 'json'
            })
                .then(response => {
                    this.histories = response.data.skus;
                    for (let i = 0; i < this.histories.length; i++) {
                        this.histories[i].url = '/detail/' + this.histories[i].id + '/';
                    }
                })
                .catch(error => {
                    console.log(error.response);
                })
        },
    }
});