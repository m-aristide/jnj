
def code_generator(diocese: str, id: int): 
    return f'{diocese.split(" ").pop()[:4].upper()}-2022-JNJ-{"0000"[0:4-len(str(id))]}{id}'


if __name__ == "__main__":
   # stuff only to run when not called via 'import' here
   print(code_generator('Diocese de Yaoundé', 1))