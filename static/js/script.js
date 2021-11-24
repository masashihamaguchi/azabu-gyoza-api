// script.js
(function () {
    'use strict'


    // for over 20 button
    const setOver20Button = function () {
        $('button').on('click', function () {
            console.log('click');
            Swal.fire({
                title: '未成年の飲酒は<br>法律で禁止されています。',
                text: '飲酒は20歳になってから。飲酒運転は法律で禁止されています。妊娠期・授乳期の飲酒は、胎児・乳児の発育に悪影響を与える恐れがあります。',
                showConfirmButton: true,
                confirmButtonText: '20歳を超えています',
                showCancelButton: true,
                cancelButtonText: 'まだ20歳ではありません',
                cancelButtonColor: '#d33',
                imageUrl: '/static/img/logo_stop_underagedrinking.svg',
                imageHeight: 200,
                imageAlt: ''
            }).then(resp => {
                console.log(resp.isConfirmed);
                if (resp.isConfirmed) window.location.href = '/adult';
            });
        });
    }

    // for onchange window size
    function screen_fit (box, player) {
        // 上下左右の縦横比を調節する関数
        let box_h = box.height(); // windowの高さを取得
        let box_w = box.width(); // windowの幅を取得
        let screen_switch = 9 / 21; // youtubeの縦横比16:9=>9/16した値
        let screen_ratio = box_h / box_w; // windowの高さの値/windowの幅の値
        let ratio_h = box_h / 9 * 21; // windowの高さ/縦横比の値
        let ratio_w = box_w / 21 * 9; // windowの幅*縦横比の値

        // 動画の縦横比とプレイヤーの縦横比を比較
        if (screen_ratio * 1000 > screen_switch * 1000) {
            player.css({
                height: "140%",
                width: ratio_h * 1.2,
                marginTop: - (box_h * 0.2),
                marginLeft: - ((ratio_h * 1.2 - box_w) / 2)
            });
        } else {
            player.css({
                width: "170%",
                height: ratio_w * 1.35,
                marginTop: - ((ratio_w * 1.35 - box_h) / 2),
                marginLeft: - (box_w * 0.35)
            });
        }
    }

    // for youtube player
    const onYouTubeIframeAPIReady = function () {
        let player = new YT.Player('gyoza_player', {
            videoId: 'ylx7M86QMAM',
            playerVars: {
                playsinline: 1,
                loop: 1,
                listType: 'playlist',
                playlist: 'ylx7M86QMAM',
                rel: 0,
                controls: 0
            },
            events: {
                'onReady': onPlayerReady,
                'onStateChange': onPlayerStateChange
            }
        });

        function onPlayerReady(event) {
            event.target.mute(); //ミュートにしないとスマホで再生されない
            event.target.playVideo(); //ビデオを再生
        }

        function onPlayerStateChange(event) {
            var ytStatus = event.target.getPlayerState();
            if (ytStatus == YT.PlayerState.ENDED) {
                event.target.mute(); //ミュートにしないとスマホで再生されない
                event.target.playVideo(); //ビデオを再生
            }
        }

    }

    // init
    $(document).ready(function () {
        // for over 20
        setOver20Button();
        // for youtube
        onYouTubeIframeAPIReady();
        // resize
        screen_fit($('#key-visual'), $('#gyoza_player'));

    });

    window.YT.ready(function(){
        // // for youtube
        // onYouTubeIframeAPIReady();
        // // resize
        // screen_fit($('#key-visual'), $('#gyoza_player'));
    });

    $(window).resize(function () {
       screen_fit($('#key-visual'), $('#gyoza_player'));
       $(window).css({ height: "100vh" });
    });
})();