import threading


def thred1():
    for i in range(100):
        print(i)

def thred2():
    i = 0
    while i<10:
        print("thred2!!")
        i+=1

# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    t1 = threading.Thread(target=thred1)
    t2 = threading.Thread(target=thred2)
    # スレッドスタート
    t1.start()
    t2.start()
