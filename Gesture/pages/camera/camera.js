Page({

  /**
   * 页面的初始数据
   */
  data: {
  init_image_array:['https://ts1.cn.mm.bing.net/th/id/R-C.8e046e136b78c4ea28bbc23d603e8d97?rik=3hzQhtkc6sghfQ&riu=http%3a%2f%2fimg.pconline.com.cn%2fimages%2fupload%2fupc%2ftx%2fwallpaper%2f1204%2f25%2fc6%2f11378613_1335369404837.jpg&ehk=DrYFgURsaLTl4Gzv3n7SXNbSZiluey7JFvi%2f5PUCeUc%3d&risl=&pid=ImgRaw&r=0','https://n.sinaimg.cn/sinakd20200412ac/100/w1600h900/20200412/be1a-isehnni3373979.jpg','https://ts1.cn.mm.bing.net/th/id/R-C.4ede019c35449ac60e900ce558862cc0?rik=oKZrtDExd2YJIQ&riu=http%3a%2f%2fimg.ugainian.com%2f443%2f5864ab17521fc.jpg&ehk=qscloAd3daz%2buDHDIJV%2bvcWU624Qgcn0ZH5m0vA6QKk%3d&risl=&pid=ImgRaw&r=0','https://img.zcool.cn/community/01f2d15befd0a0a80120925224c440.jpg@1280w_1l_2o_100sh.jpg','https://ts1.cn.mm.bing.net/th/id/R-C.5f8657d79d3269925a95535de3bb1a07?rik=obFPN%2b4a4iaCCA&riu=http%3a%2f%2fncimg1.nextcar.cn%2fcontent%2f2020-12-17%2f7ef6b2e7-48f7-4ae0-b97c-d8eff2cd841e.jpg&ehk=%2baHybZ1SJSDW7E8wuy6%2bBm03%2b8EGzeoVerq5qfCkzA4%3d&risl=&pid=ImgRaw&r=0','https://www.2008php.com/2015_Website_appreciate/2015-03-21/20150321002816.jpg','https://www.2008php.com/2012_Website_appreciate/2012-06-08/20120608020743.jpg','https://pic.52112.com/180531/JPG-180531_495/torUsXlcSF_small.jpg'],
  init_image : '',
  init_image_index : Math.floor(Math.random() * 8),
  base64Img:'',
  result:'',
  }, 
  //选择图片
  imgSelect(){
    var that = this;
    //调用相机
    wx.chooseMedia({
      count: 1,
      sizeType:['original', 'compressed'],
      sourceType:['album', 'camera'],
      success:(res)=>{
        // console.log(res.tempFiles[0].tempFilePath)
        const tempFiles = res.tempFiles[0]
        that.setData({
        //  init_image_index : 0,
        //  init_image : tempFiles.tempFilePath
          init_image : res.tempFiles[0].tempFilePath
        })
        wx.downloadFile({
          url: res.tempFiles[0].tempFilePath,
          filePath: wx.env.USER_DATA_PATH+ '/temp.jpg',
          success: function(res) {
            console.log('downloadFile  success', res);
          },
          fail: function(err) {
            console.log('downloadFile  fail', err);
          }
        });
        that.getB64ByPath(tempFiles.tempFilePath)
      //  console.log(tempFiles.tempFilePath)
      }
    }) 
  },
   //图片转为base64
  getB64ByPath(path){
    var that = this
    wx.getFileSystemManager().readFile({
      filePath:path,
      encoding:'base64',
      success:(res)=>{
        that.setData({
          base64Img : res.data
        })
      }
    })
  },
  plant(){
    var that = this;
    wx.showLoading({  // 显示加载中loading效果 
      title: "识别中",
      mask: true  //开启蒙版遮罩
    });
    wx.request({
      url: 'http://127.0.0.1:8000/weixin_api/hello/',
      data:{ 
        //img_path : this.init_image,
        image_base64 : that.data.base64Img
      },
      header: {
        "Content-type": "application/x-www-form-urlencoded" 
      },
      method:'POST',
      success(res){
        console.log(res.data)
        that.setData({
          result : res.data
        })
        wx.hideLoading();
      }
    })
  },
 
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    //设置初始图片
    this.setData({
      init_image : this.data.init_image_array[this.data.init_image_index]
    })
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady() {
    
  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow() {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide() {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload() {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh() {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom() {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage() {

  }
})