import os
import re
import time
import sys
import getopt
from string import digits
from util.Util import Util


class SeqCounter:
    def __init__(self):
        self.setting_json = Util.load_setting()
        # print(self.setting_json)
        # self.seq_path = './seqs/'
        self.encoding = self.setting_json['seqCounter']['encoding']
        self.seq_path = self.setting_json['seqCounter']['inputOptions']['seqPath']
        # self.result_path = './results/'
        self.result_path = self.setting_json['seqCounter']['outputOptions']['resultPath']
        self.time_str = str(time.strftime('%Y%m%d%H%M%S', time.localtime()))
        self.save_file = 'result' + self.time_str + self.setting_json['seqCounter']['outputOptions'][
            'resultExtensionName']
        # self.seq_type_file_path = './virusinfo.ini'
        self.seq_type_file_path = self.setting_json['seqCounter']['constraintOptions']['seqTypeList']
        self.virus_info_list = []
        self.check_type_flag = bool(self.setting_json['seqCounter']['constraintOptions']['seqTypeCheck'])

    def read_path(self):
        if not os.path.isdir(self.seq_path):
            print("错误：指定源文件参数不是目录。")
            return False
        if not os.path.exists(self.seq_path):
            print("错误：指定的源文件目录不存在。")
            return False
        all_file_name_list = os.listdir(self.seq_path)
        if len(all_file_name_list) <= 0:
            print("错误：指定的源文件目录为空。")
            return False
        file_name_list = []
        for file_name in all_file_name_list:
            ex_name_list = re.findall(r'\.[^.\\/:*?"<>|\r\n]+$', file_name)
            if len(ex_name_list) <= 0:
                continue
            ex_name = re.findall(r'\.[^.\\/:*?"<>|\r\n]+$', file_name)[0]
            if ex_name != '.txt':
                continue
            file_name_list.append(file_name)
        if len(file_name_list) <= 0:
            print("错误：指定的源文件目录没有任何目标文件。")
            return False
        return file_name_list

    def read_virusinfo(self):
        if not os.path.exists(self.seq_type_file_path):
            print("警告：类型约束文件不存在，将跳过类型判断。")
            return False
        with open('virusinfo.ini', 'r', encoding=self.encoding) as file:
            content = file.read()
            if not content or len(content) <= 0:
                print("警告：类型约束文件内容为空，将跳过类型判断。")
                return False
            virus_info_str = content.replace(' ', '').replace('\n', '').replace('\t', '')
            if not virus_info_str or len(virus_info_str) <= 0:
                print("警告：类型约束文件内容为空，将跳过类型判断。")
                return False
            pre_virus_info_list = virus_info_str.split(',')
            if not pre_virus_info_list or len(pre_virus_info_list) <= 0:
                print("警告：类型约束文件内容为空，将跳过类型判断。")
                return False
            virus_info_list = []
            index = 0
            for pre_virus_info in pre_virus_info_list:
                index += 1
                if not pre_virus_info or len(pre_virus_info) <= 0:
                    print("警告：第[" + str(index) + '行参数不合法，已忽略。')
                    continue
                virus_infos = pre_virus_info.split('-')
                if not virus_infos or len(virus_infos) != 2:
                    print("警告：第[" + str(index) + '行参数不合法，已忽略。')
                    continue
                item = {}
                item['virus_name'] = virus_infos[0]
                virus_lens = virus_infos[1].split('/')
                if not virus_lens or len(virus_infos) <= 0:
                    print("警告：第[" + str(index) + '行参数，病毒长度不合法，已忽略。')
                    continue
                item['virus_lens'] = virus_lens
                virus_info_list.append(item)
            return virus_info_list

    def checkSeqType(self, length):
        if not self.virus_info_list or len(self.virus_info_list) <= 0:
            return '未知'
        for virus_info in self.virus_info_list:
            if str(length) in virus_info['virus_lens']:
                return virus_info['virus_name']
        return '未知'

    def statistics(self):
        file_name_list = self.read_path()
        if not file_name_list:
            print("错误：读取源文件列表失败。")
            return False
        self.check_type_flag = True
        self.virus_info_list = self.read_virusinfo()
        if not self.virus_info_list or len(self.virus_info_list) <= 0:
            self.check_type_flag = False
        print("开始分析，一共" + str(len(file_name_list)) + "个文件。")
        file_index = 1
        result_list = []
        for file_name in file_name_list:
            full_path = os.path.join(self.seq_path, file_name)
            if not os.path.exists(full_path):
                print("\t警告：源文件[" + full_path + "]不存在。直接跳过。")
                continue
            item = {}
            item['file_index'] = file_index
            item['file_name'] = file_name
            seq_str_list = []
            with open(full_path, 'r', encoding=self.encoding) as file:
                content = file.read()
                if (not content or len(content) <= 0):
                    print("\t警告：源文件[" + full_path + "]内容为空。直接跳过。")
                    continue
                seq_str_list = content.split('>')
                if len(seq_str_list) <= 0:
                    print("\t警告：源文件[" + full_path + "]中不存在任何序列。直接跳过。")
                    continue
                item['seq_num'] = len(seq_str_list) - 1
            seq_index = 1
            seq_name_reg = '(.*?)\n'
            seq_list = []
            for seq_str in seq_str_list:
                if len(seq_str) <= 0:
                    continue
                seq_name_pattern = re.compile(seq_name_reg, re.S)
                seq_name_list = seq_name_pattern.findall(seq_str)
                if len(seq_name_list) <= 0:
                    print("警告：第" + str(seq_index) + "个序列解析失败：序列名称不存在。")
                    continue
                seq_item = {}
                seq_name = seq_name_list[0]
                seq_body = seq_str[len(seq_name):].replace(' ', '').replace('\n', '')
                table = seq_body.maketrans('', '', digits)
                seq_body = seq_body.translate(table)
                seq_item['seq_index'] = seq_index
                seq_item['seq_name'] = seq_name
                seq_item['seq_length'] = len(seq_body)
                if self.check_type_flag:
                    seq_item['virus_name'] = self.checkSeqType(seq_item['seq_length'])
                seq_list.append(seq_item)
                seq_index = seq_index + 1
            item['seq_list'] = seq_list
            result_list.append(item)
            file_index += 1
        return result_list

    def show_result(self, result_list):
        if not result_list or len(result_list) <= 0:
            return False
        for result in result_list:
            print("文件" + str(result['file_index']) + "：\n\t文件名：" + result['file_name'])
            print("\t序列数：" + str(result['seq_num']))
            seq_list = result['seq_list']
            if self.check_type_flag:
                for seq in seq_list:
                    print("\t序号" + str(seq['seq_index']) + "， 序列名称：" + seq['seq_name'] + "， 长度：" + str(
                        seq['seq_length']) + ', 类型：' + seq['virus_name'])
            else:
                for seq in seq_list:
                    print(
                        "\t序号" + str(seq['seq_index']) + "， 序列名称：" + seq['seq_name'] + "， 长度：" + str(seq['seq_length']))
        return True

    def save_result(self, result_list):
        if not result_list or len(result_list) <= 0:
            return False
        with open(self.result_path + self.save_file, 'w', encoding=self.encoding) as file:
            for result in result_list:
                file.write("文件" + str(result['file_index']) + "：\n\t文件名：" + result['file_name'] + "\n")
                file.write("\t序列数：" + str(result['seq_num']) + "\n")
                seq_list = result['seq_list']
                for seq in seq_list:
                    if self.check_type_flag:
                        file.write("\t序号" + str(seq['seq_index']) + "， 序列名称：" + seq['seq_name'] + "， 长度：" + str(
                            seq['seq_length']) + ', 类型：' + seq['virus_name'] + "\n")
                    else:
                        file.write("\t序号" + str(seq['seq_index']) + "， 序列名称：" + seq['seq_name'] + "， 长度：" + str(
                            seq['seq_length']) + "\n")
        return True

    # 入口函数
    def run(self):
        result_list = self.statistics()
        self.show_result(result_list)
        self.save_result(result_list)
        print()
        print("-" * 50)
        print("统计完毕，结果已保存于[" + self.result_path + self.save_file + "]中。")
        print("请使用任意文本编辑器打开查看。")
        print("-" * 50)

    def getArgs(self, argv):
        input_path = self.seq_path
        output_path = self.result_path
        try:
            opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
        except getopt.GetoptError:
            print('SeqCounter.py -i <inputfile> -o <outputfile>')
            sys.exit(2)
        for opt, arg in opts:
            if opt == '-h':
                print('SeqCounter.py -i <inputfile> -o <outputfile>')
                sys.exit()
            elif opt in ("-i", "--ifile"):
                input_path = arg
            elif opt in ("-o", "--ofile"):
                output_path = arg
        self.seq_path = input_path
        self.result_path = output_path
        print('输入文件目录：', input_path)
        print('输出文件目录：', output_path)


# 运行
if __name__ == '__main__':
    seqCounter = SeqCounter()
    seqCounter.getArgs(sys.argv[1:])
    seqCounter.run()
