import os,json, pandas as pd


def dummy_excel(in_file):
    d_frame = pd.read_excel(io=in_file,sheet_name='Sheet1')
    print(d_frame.head(5))

def process_excel(file_path):
    print(file_path)
    df = pd.read_excel(io=file_path,sheet_name='Sheet1')
    df_new = df[1:2]
    data = df_new.to_dict('records')
    return data

def create_json(car_model):

    json_data = {}
    for car in car_model:
        car_folder = os.path.join(root_folder,car)
        if os.path.join(car_folder):
            #print(f"The folder exists which is {car_folder}")
            json_data[car] = {}
            for file in os.listdir(car_folder):
                if file.endswith('.xlsx'):
                    category = file.split('.')[0]
                    car_data = process_excel(os.path.join(car_folder,file))
                    json_data[car][category] = car_data

    return json_data



if __name__ == "__main__":
    
    root_folder = ''#submit the folder path
    out_path = ''#submit the folder path
    car_model = os.listdir(root_folder)
    json_data = create_json(car_model)
    print(json_data)
    with open(out_path,"w") as f:
        json.dump(json_data,f,indent=4)
    

