import os


def write_chat_msg(filename,text_msg):
    # 写数据
    file_object = open(filename, 'a+')
    file_object.writelines("\n"+text_msg)
    file_object.close()


def renamefile():
    filename = '181228-162717.gif'
    src = '/Users/daiwen/Documents/wechat/'
    dst = '/Users/daiwen/Documents/wechat/recall/'
    os.rename(src+filename,dst+filename)
if __name__ == '__main__':
    write_chat_msg("1111")
    write_chat_msg("222")
    write_chat_msg("33333")