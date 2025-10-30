// ==UserScript==
// @name         TurbowarpProjectLockerBreaker
// @description  用于破解YL_YOLO的Scratch作品加密插件，不得用于非法用途！！！
// @namespace    http://tampermonkey.net/
// @version      1.0
// @match        *://yunpa.vip/*
// @match        *://turbowarp.org/*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    //实现反防篡改
    const OriginalMutationObserver = window.MutationObserver || window.WebKitMutationObserver;
    window.MutationObserver = function(callback) {
        console.log('检测到 MutationObserver 创建');
        const callbackStr = callback.toString();
        const blockedPatterns = [
            /removedNodes.*includes.*overlay/,
            /removedNodes.*includes.*backgroundClone/,
            /showPasswordScreen/
        ];
        if (blockedPatterns.some(pattern => pattern.test(callbackStr))) {
            console.log('已拦截防护性 MutationObserver');
            return {
                observe: function() {
                    console.log('假的 observe 方法被调用');
                },
                disconnect: function() {
                    console.log('假的 disconnect 方法被调用');
                },
                takeRecords: function() {
                    console.log('假的 takeRecords 方法被调用');
                    return [];
                }
            };
        }
        return new OriginalMutationObserver(callback);
    };
    window.MutationObserver.prototype = OriginalMutationObserver.prototype;

    //实现清除遮罩层
    const intervalId = setInterval(() => {
        var bg_div = document.querySelector('div[class^="bg_cls_"]');
        var overlay_div = document.querySelector('div[class^="overlay_cls_"]');
        if (bg_div != undefined && overlay_div != undefined) {
            bg_div.remove();
            overlay_div.remove();
            resetEventListener();
        }else {
            console.log("未检测到输入密码的界面");
        }
    }, 250);

    //在程序结束时将循环结束
    window.addEventListener('beforeunload', () => {
        clearInterval(intervalId);
    });

    //恢复按键等功能
    function resetEventListener(){
        document.addEventListener('keydown', function(e) {
            e.stopPropagation();
        }, true);
        document.addEventListener('contextmenu', function(e) {
            e.stopPropagation();
        }, true);
        document.addEventListener('selectstart', function(e) {
            e.stopPropagation();
        }, true);
        document.addEventListener('dragstart', function(e) {
            e.stopPropagation();
        }, true);
    }
})();
