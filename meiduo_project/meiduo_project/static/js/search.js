let vm = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    data: {
        username: getCookie('username'),

    },
    mounted() {

    },
    methods: {
        // 加入购物车
        add_carts(sku_id) {
            let url = '/carts/';
            axios.post(url, {
                sku_id: sku_id,
                count: 1
            }, {
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                },
                responseType: 'json',
                withCredentials: true
            })
                .then(response => {
                    if (response.data.code == '0') {
                        alert('添加购物车成功');

                    } else { // 参数错误
                        alert(response.data.errmsg);
                    }
                })
                .catch(error => {
                    console.log(error.response);
                })
        },
    }
});