
class ManagemenFile :
    def read_file(self,filename):
        # dega file.readlines hasilnya dalam bentuk list = ['sds','dat']
        try:
            with open(filename, mode='r') as file:
                data = file.readlines().rstrip('\n')
                print("data nay",data)
            return data
        except FileNotFoundError:
            return f"File {filename} tidak  found."
        except Exception as e:
            return f"An error occurred: {str(e)}"
    def write_file(self,data,filename):
        try:
            with open(filename, mode='w') as file:
                file.write(data)
            return f"Data has been saved to {filename}."
        except Exception as e:
            return f"An error occurred: {str(e)}"
        
# coba dulu abg da
ManagemenFile().read_file('dar1.txt')