{"metadata":{"kernelspec":{"language":"python","display_name":"Python 3","name":"python3"},"language_info":{"name":"python","version":"3.10.12","mimetype":"text/x-python","codemirror_mode":{"name":"ipython","version":3},"pygments_lexer":"ipython3","nbconvert_exporter":"python","file_extension":".py"},"kaggle":{"accelerator":"none","dataSources":[{"sourceId":57891,"databundleVersionId":7056235,"sourceType":"competition"}],"dockerImageVersionId":30587,"isInternetEnabled":false,"language":"python","sourceType":"notebook","isGpuEnabled":false}},"nbformat_minor":4,"nbformat":4,"cells":[{"source":"<a href=\"https://www.kaggle.com/code/ameyck/optiver-trading?scriptVersionId=202451829\" target=\"_blank\"><img align=\"left\" alt=\"Kaggle\" title=\"Open in Kaggle\" src=\"https://kaggle.com/static/images/open-in-kaggle.svg\"></a>","metadata":{},"cell_type":"markdown"},{"cell_type":"code","source":"import numpy as np # linear algebra\nimport pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)\nimport os\nimport joblib\nimport warnings\nimport gc\nimport joblib\n\nwarnings.filterwarnings('ignore')","metadata":{"_uuid":"8f2839f25d086af736a60e9eeb907d3b93b6e0e5","_cell_guid":"b1076dfc-b9ad-4769-8c92-a6c4dae69d19","execution":{"iopub.status.busy":"2024-10-21T09:54:37.240701Z","iopub.execute_input":"2024-10-21T09:54:37.241146Z","iopub.status.idle":"2024-10-21T09:54:37.671276Z","shell.execute_reply.started":"2024-10-21T09:54:37.241099Z","shell.execute_reply":"2024-10-21T09:54:37.670244Z"},"trusted":true},"execution_count":1,"outputs":[]},{"cell_type":"code","source":"df=pd.read_csv('/kaggle/input/optiver-trading-at-the-close/train.csv')\ndf.sort_values(by='date_id',ascending=True)\ndf.reset_index(drop=True,inplace=True)\ndf.head()","metadata":{"execution":{"iopub.status.busy":"2024-10-21T09:54:37.673258Z","iopub.execute_input":"2024-10-21T09:54:37.673865Z","iopub.status.idle":"2024-10-21T09:54:58.091058Z","shell.execute_reply.started":"2024-10-21T09:54:37.67382Z","shell.execute_reply":"2024-10-21T09:54:58.089861Z"},"trusted":true},"execution_count":2,"outputs":[{"execution_count":2,"output_type":"execute_result","data":{"text/plain":"   stock_id  date_id  seconds_in_bucket  imbalance_size  \\\n0         0        0                  0      3180602.69   \n1         1        0                  0       166603.91   \n2         2        0                  0       302879.87   \n3         3        0                  0     11917682.27   \n4         4        0                  0       447549.96   \n\n   imbalance_buy_sell_flag  reference_price  matched_size  far_price  \\\n0                        1         0.999812   13380276.64        NaN   \n1                       -1         0.999896    1642214.25        NaN   \n2                       -1         0.999561    1819368.03        NaN   \n3                       -1         1.000171   18389745.62        NaN   \n4                       -1         0.999532   17860614.95        NaN   \n\n   near_price  bid_price  bid_size  ask_price   ask_size  wap    target  \\\n0         NaN   0.999812  60651.50   1.000026    8493.03  1.0 -3.029704   \n1         NaN   0.999896   3233.04   1.000660   20605.09  1.0 -5.519986   \n2         NaN   0.999403  37956.00   1.000298   18995.00  1.0 -8.389950   \n3         NaN   0.999999   2324.90   1.000214  479032.40  1.0 -4.010200   \n4         NaN   0.999394  16485.54   1.000016     434.10  1.0 -7.349849   \n\n   time_id row_id  \n0        0  0_0_0  \n1        0  0_0_1  \n2        0  0_0_2  \n3        0  0_0_3  \n4        0  0_0_4  ","text/html":"<div>\n<style scoped>\n    .dataframe tbody tr th:only-of-type {\n        vertical-align: middle;\n    }\n\n    .dataframe tbody tr th {\n        vertical-align: top;\n    }\n\n    .dataframe thead th {\n        text-align: right;\n    }\n</style>\n<table border=\"1\" class=\"dataframe\">\n  <thead>\n    <tr style=\"text-align: right;\">\n      <th></th>\n      <th>stock_id</th>\n      <th>date_id</th>\n      <th>seconds_in_bucket</th>\n      <th>imbalance_size</th>\n      <th>imbalance_buy_sell_flag</th>\n      <th>reference_price</th>\n      <th>matched_size</th>\n      <th>far_price</th>\n      <th>near_price</th>\n      <th>bid_price</th>\n      <th>bid_size</th>\n      <th>ask_price</th>\n      <th>ask_size</th>\n      <th>wap</th>\n      <th>target</th>\n      <th>time_id</th>\n      <th>row_id</th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <th>0</th>\n      <td>0</td>\n      <td>0</td>\n      <td>0</td>\n      <td>3180602.69</td>\n      <td>1</td>\n      <td>0.999812</td>\n      <td>13380276.64</td>\n      <td>NaN</td>\n      <td>NaN</td>\n      <td>0.999812</td>\n      <td>60651.50</td>\n      <td>1.000026</td>\n      <td>8493.03</td>\n      <td>1.0</td>\n      <td>-3.029704</td>\n      <td>0</td>\n      <td>0_0_0</td>\n    </tr>\n    <tr>\n      <th>1</th>\n      <td>1</td>\n      <td>0</td>\n      <td>0</td>\n      <td>166603.91</td>\n      <td>-1</td>\n      <td>0.999896</td>\n      <td>1642214.25</td>\n      <td>NaN</td>\n      <td>NaN</td>\n      <td>0.999896</td>\n      <td>3233.04</td>\n      <td>1.000660</td>\n      <td>20605.09</td>\n      <td>1.0</td>\n      <td>-5.519986</td>\n      <td>0</td>\n      <td>0_0_1</td>\n    </tr>\n    <tr>\n      <th>2</th>\n      <td>2</td>\n      <td>0</td>\n      <td>0</td>\n      <td>302879.87</td>\n      <td>-1</td>\n      <td>0.999561</td>\n      <td>1819368.03</td>\n      <td>NaN</td>\n      <td>NaN</td>\n      <td>0.999403</td>\n      <td>37956.00</td>\n      <td>1.000298</td>\n      <td>18995.00</td>\n      <td>1.0</td>\n      <td>-8.389950</td>\n      <td>0</td>\n      <td>0_0_2</td>\n    </tr>\n    <tr>\n      <th>3</th>\n      <td>3</td>\n      <td>0</td>\n      <td>0</td>\n      <td>11917682.27</td>\n      <td>-1</td>\n      <td>1.000171</td>\n      <td>18389745.62</td>\n      <td>NaN</td>\n      <td>NaN</td>\n      <td>0.999999</td>\n      <td>2324.90</td>\n      <td>1.000214</td>\n      <td>479032.40</td>\n      <td>1.0</td>\n      <td>-4.010200</td>\n      <td>0</td>\n      <td>0_0_3</td>\n    </tr>\n    <tr>\n      <th>4</th>\n      <td>4</td>\n      <td>0</td>\n      <td>0</td>\n      <td>447549.96</td>\n      <td>-1</td>\n      <td>0.999532</td>\n      <td>17860614.95</td>\n      <td>NaN</td>\n      <td>NaN</td>\n      <td>0.999394</td>\n      <td>16485.54</td>\n      <td>1.000016</td>\n      <td>434.10</td>\n      <td>1.0</td>\n      <td>-7.349849</td>\n      <td>0</td>\n      <td>0_0_4</td>\n    </tr>\n  </tbody>\n</table>\n</div>"},"metadata":{}}]},{"cell_type":"markdown","source":"# Data Cleaning","metadata":{}},{"cell_type":"code","source":"# df.shape (5237980, 17)\ndf= df.dropna(subset=['target'],axis=0) # drop rows where taget is nan\ndf.drop_duplicates(inplace=True)\n# df.shape (5237980, 17)\ndf.reset_index(drop=True,inplace=True)\n# Reduce Memory Usage \n\ndef mem_usage(df):\n    start_mem = df.memory_usage().sum() / 1024**2  # Total memory in MB\n\n    for col in df.columns:\n        print(f\"Processing column: {col}, dtype: {df[col].dtype}\")  # Debugging output\n        col_type = df[col].dtype\n        \n        # Check for integer types\n        if np.issubdtype(col_type, np.integer):\n            c_min = df[col].min()\n            c_max = df[col].max()\n            if c_min >= np.iinfo(np.int8).min and c_max <= np.iinfo(np.int8).max:\n                df[col] = df[col].astype(np.int8)\n            elif c_min >= np.iinfo(np.int16).min and c_max <= np.iinfo(np.int16).max:\n                df[col] = df[col].astype(np.int16)\n            elif c_min >= np.iinfo(np.int32).min and c_max <= np.iinfo(np.int32).max:\n                df[col] = df[col].astype(np.int32)\n            else:\n                df[col] = df[col].astype(np.int64)\n\n        # Check for float types\n        elif np.issubdtype(col_type, np.floating):\n            c_min = df[col].min()\n            c_max = df[col].max()\n            if c_min >= np.finfo(np.float16).min and c_max <= np.finfo(np.float16).max:\n                df[col] = df[col].astype(np.float32) # numba is not supporting float16\n            elif c_min >= np.finfo(np.float32).min and c_max <= np.finfo(np.float32).max:\n                df[col] = df[col].astype(np.float32)\n            else:\n                df[col] = df[col].astype(np.float64)\n\n    end_mem = df.memory_usage().sum() / 1024**2\n    print(f\"Memory usage reduced from {start_mem:.2f} MB to {end_mem:.2f} MB\")\n    print(f\"Decrease: {100 * (start_mem - end_mem) / start_mem:.2f}%\")\n    \n    return df\n\ndf = mem_usage(df)","metadata":{"execution":{"iopub.status.busy":"2024-10-21T09:54:58.092457Z","iopub.execute_input":"2024-10-21T09:54:58.092796Z","iopub.status.idle":"2024-10-21T09:55:13.588566Z","shell.execute_reply.started":"2024-10-21T09:54:58.092768Z","shell.execute_reply":"2024-10-21T09:55:13.587336Z"},"trusted":true},"execution_count":3,"outputs":[{"name":"stdout","text":"Processing column: stock_id, dtype: int64\nProcessing column: date_id, dtype: int64\nProcessing column: seconds_in_bucket, dtype: int64\nProcessing column: imbalance_size, dtype: float64\nProcessing column: imbalance_buy_sell_flag, dtype: int64\nProcessing column: reference_price, dtype: float64\nProcessing column: matched_size, dtype: float64\nProcessing column: far_price, dtype: float64\nProcessing column: near_price, dtype: float64\nProcessing column: bid_price, dtype: float64\nProcessing column: bid_size, dtype: float64\nProcessing column: ask_price, dtype: float64\nProcessing column: ask_size, dtype: float64\nProcessing column: wap, dtype: float64\nProcessing column: target, dtype: float64\nProcessing column: time_id, dtype: int64\nProcessing column: row_id, dtype: object\nMemory usage reduced from 679.35 MB to 304.71 MB\nDecrease: 55.15%\n","output_type":"stream"}]},{"cell_type":"markdown","source":"# Parallel triplet imbalance calculation","metadata":{}},{"cell_type":"code","source":"from numba import njit, prange\nfrom itertools import combinations\n\n@njit(parallel=True)\n\ndef compute_triplet_imbalance(df_values,comb_indices):\n    num_row=df_values.shape[0]\n    num_comb=len(comb_indices)\n    imbalance_features=np.empty((num_row,num_comb))\n    \n    for i in prange(num_comb):\n        a,b,c=comb_indices[i]\n        \n        for j in range(num_row):\n            max_val=max(df_values[j,a],df_values[j,b],df_values[j,c])\n            min_val=min(df_values[j,a],df_values[j,b],df_values[j,c])\n            mid_val=df_values[j,a]+df_values[j,b]+df_values[j,c]-min_val-max_val\n            \n            if min_val==mid_val:\n                imbalance_features[j,i]=np.nan\n            else:\n                imbalance_features[j,i]=(max_val-mid_val)/(mid_val-min_val)\n            \n    return imbalance_features\n        \n\ndef calcul_triplet_imbalance(price,df):\n    df_values=df[price].values\n    comb_indices=np.array([(price.index(a),price.index(b),price.index(c)) for a,b,c in combinations(price,3)],dtype=np.int64)\n#     print(comb_indices)\n    feature_array=compute_triplet_imbalance(df_values,comb_indices)\n\n    columns=[f'{a}_{b}_{c}_imb' for a,b,c in combinations(price,3)]\n    features=pd.DataFrame(feature_array,columns=columns)\n    return features\n    ","metadata":{"execution":{"iopub.status.busy":"2024-10-21T09:55:13.59079Z","iopub.execute_input":"2024-10-21T09:55:13.59118Z","iopub.status.idle":"2024-10-21T09:55:15.029831Z","shell.execute_reply.started":"2024-10-21T09:55:13.591146Z","shell.execute_reply":"2024-10-21T09:55:15.028681Z"},"trusted":true},"execution_count":4,"outputs":[]},{"cell_type":"markdown","source":"# Feature generation func","metadata":{}},{"cell_type":"code","source":"def imbalance_features(df):\n    prices=[\"reference_price\", \"far_price\", \"near_price\", \"ask_price\", \"bid_price\", \"wap\"]\n    sizes = [\"matched_size\", \"bid_size\", \"ask_size\", \"imbalance_size\"]\n    \n    df['volume']= df.eval('ask_size + bid_size')\n    df['mid_price']= df.eval('(ask_price + bid_price)/2')\n    df['liquidity_imbalance']= df.eval('(bid_size - ask_size)/(bid_size + ask_size)')\n    df['matched_imbalance']= df.eval('(imbalance_size - matched_size)/(imbalance_size + matched_size)')\n    df['size_imbalance']= df.eval('bid_size/ask_size')\n    \n    for c in combinations(prices,2):\n        df[f'{c[0]}_{c[1]}_imb']= df.eval(f'({c[0]}-{c[1]})/({c[0]}+{c[1]})')\n# considering 3 features at a time and finding their relationships\n    for c in [['ask_price', 'bid_price', 'wap', 'reference_price'], sizes]:\n        triplet_feature=calcul_triplet_imbalance(c,df)\n        df[triplet_feature.columns]=triplet_feature.values\n      # new features\n        df['imbalance_momentum']=df.groupby(['stock_id'])['imbalance_size'].diff(periods=1)/df['matched_size']\n        df['price_spread']=df['ask_price']-df['bid_size']\n        df[\"spread_intensity\"] = df.groupby(['stock_id'])['price_spread'].diff()\n        df['price_pressure'] = df['imbalance_size'] * (df['ask_price'] - df['bid_price'])\n        df['market_urgency'] = df['price_spread'] * df['liquidity_imbalance']\n        df['depth_pressure'] = (df['ask_size'] - df['bid_size']) * (df['far_price'] - df['near_price'])\n    \n    #measures of all cols of single row\n    for func in [\"mean\", \"std\", \"skew\", \"kurt\"]:\n        df[f\"all_prices_{func}\"] = df[prices].agg(func, axis=1)\n        df[f\"all_sizes_{func}\"] = df[sizes].agg(func, axis=1)\n        \n    # lag features and % change in values over the given time frame\n    for col in ['matched_size', 'imbalance_size', 'reference_price', 'imbalance_buy_sell_flag']:\n        for window in [1,2,5,10]:\n            df[f'{col}_shift_{window}']=df.groupby(['stock_id'])[col].shift(window)\n            df[f'{col}_return_{window}']=df.groupby(['stock_id'])[col].pct_change(window)\n    \n    for col in ['ask_price', 'bid_price', 'ask_size', 'bid_size']:\n        for window in [1,2,5,10]:\n            df[f'{col}_diff_{window}']=df.groupby(['stock_id'])[col].diff(window)\n    df.replace([np.inf,-np.inf],np.nan,inplace=True)\n    return df","metadata":{"execution":{"iopub.status.busy":"2024-10-21T09:55:15.031205Z","iopub.execute_input":"2024-10-21T09:55:15.031533Z","iopub.status.idle":"2024-10-21T09:55:15.045079Z","shell.execute_reply.started":"2024-10-21T09:55:15.031504Z","shell.execute_reply":"2024-10-21T09:55:15.043705Z"},"trusted":true},"execution_count":5,"outputs":[]},{"cell_type":"code","source":"def other_features(df):\n    df['day_of_wk']=(df['date_id'])%5\n    df['seconds']=df['seconds_in_bucket']%60\n    df['minute']=df['seconds_in_bucket']//60\n    \n#     for k,v in global_stock_id_feats.items():\n#         df[f'global_{key}']=df['stock_id'].map(value.to_dict())\n    return df\n\ndef generate_all_features(df):\n    cols = [c for c in df.columns if c not in ['row_id','time_id','target']]\n    df=df[cols]\n    df=imbalance_features(df)\n    df=other_features(df)\n    gc.collect()\n    feature_name=[i for i in df.columns if i not in ['row_id','date_id','target','time_id']]\n    return df[feature_name]","metadata":{"execution":{"iopub.status.busy":"2024-10-21T09:55:15.046817Z","iopub.execute_input":"2024-10-21T09:55:15.047301Z","iopub.status.idle":"2024-10-21T09:55:15.063616Z","shell.execute_reply.started":"2024-10-21T09:55:15.047259Z","shell.execute_reply":"2024-10-21T09:55:15.062621Z"},"trusted":true},"execution_count":6,"outputs":[]},{"cell_type":"code","source":"# Splitting data\nsplit_day=435\ndate_ids=df['date_id'].values\ndf_train=df[df['date_id']<=split_day]\ndf_test=df[df['date_id']>split_day]","metadata":{"execution":{"iopub.status.busy":"2024-10-21T09:55:15.065117Z","iopub.execute_input":"2024-10-21T09:55:15.066063Z","iopub.status.idle":"2024-10-21T09:55:15.806074Z","shell.execute_reply.started":"2024-10-21T09:55:15.06602Z","shell.execute_reply":"2024-10-21T09:55:15.804721Z"},"trusted":true},"execution_count":7,"outputs":[]},{"cell_type":"code","source":"# df[df['date_id']>435].count() #494999\n# df[df['date_id']<=435].count() #4742893\nstart=0\nend=480//5\npurged_set =(\n(date_ids>= start-2) & (date_ids<=start+2)|\n(date_ids>= end-2) & (date_ids<=end+2)\n)\n\ntest_indices = (date_ids>=start) & (date_ids<end) & (date_ids>split_day) &  ~purged_set\ntrain_indices= ~test_indices & ~purged_set & date_ids<=split_day\nprint(len(test_indices),len(train_indices))","metadata":{"execution":{"iopub.status.busy":"2024-10-21T09:55:15.807356Z","iopub.execute_input":"2024-10-21T09:55:15.80768Z","iopub.status.idle":"2024-10-21T09:55:15.842473Z","shell.execute_reply.started":"2024-10-21T09:55:15.807652Z","shell.execute_reply":"2024-10-21T09:55:15.841206Z"},"trusted":true},"execution_count":8,"outputs":[{"name":"stdout","text":"5237892 5237892\n","output_type":"stream"}]},{"cell_type":"code","source":"df_train_feats=generate_all_features(df_train)\ndf_test_feats=generate_all_features(df_test)\n# len(df_test_feats)","metadata":{"execution":{"iopub.status.busy":"2024-10-21T09:55:15.843905Z","iopub.execute_input":"2024-10-21T09:55:15.844238Z","iopub.status.idle":"2024-10-21T09:55:57.911334Z","shell.execute_reply.started":"2024-10-21T09:55:15.844208Z","shell.execute_reply":"2024-10-21T09:55:57.910162Z"},"trusted":true},"execution_count":9,"outputs":[]},{"cell_type":"markdown","source":"# Model Training","metadata":{}},{"cell_type":"code","source":"import lightgbm as lgb\nfrom sklearn.metrics import mean_absolute_error\n\nlgb_params={\n    'objective':'mae',\n    'n_estimators':5000,\n    'num_leaves':250,\n    'learning_rate':0.008,\n    'n_jobs':4,\n    'verbosity':-1,\n    'importance_type':'gain'\n    \n}\nfeature_name=list(df_train_feats.columns)\n# print(feature_name)\n\nmodels=[]\nscore=[]\n\n# saving models \n# model_save_path='/kaggle/input/optiver-trading-at-the-close/'\n# if not model_save_path:\n#     os.makedirs(model_save_path)\n\n\n    \ndf_fold_train= df_train_feats\ndf_fold_train_target=df_train['target']\n\n\ndf_fold_test=df_test_feats\ndf_fold_test_target=df_test['target']\n\n\nlgb_model=lgb.LGBMRegressor(**lgb_params)\nlgb_model.fit(df_fold_train[feature_name],df_fold_train_target,\n             eval_set=[(df_fold_test[feature_name],df_fold_test_target)],\n              callbacks=[lgb.callback.early_stopping(stopping_rounds=100),\n                        lgb.callback.log_evaluation(period=100)]\n             )\n\nmodels.append(lgb_model)\n# model_filename=os.path.join(model_save_path,f'1.txt')\n# lgb_model.booster_.save_model(model_filename)\n\nfold_predictions = lgb_model.predict(df_fold_test[feature_name])\nfold_score=mean_absolute_error(fold_predictions,df_fold_test_target)\nscore.append(fold_score)\nprint(f'MAE : {fold_score}')\n","metadata":{"execution":{"iopub.status.busy":"2024-10-21T09:55:57.914002Z","iopub.execute_input":"2024-10-21T09:55:57.914378Z","iopub.status.idle":"2024-10-21T11:02:27.963441Z","shell.execute_reply.started":"2024-10-21T09:55:57.914344Z","shell.execute_reply":"2024-10-21T11:02:27.961964Z"},"trusted":true},"execution_count":10,"outputs":[{"name":"stdout","text":"Training until validation scores don't improve for 100 rounds\n[100]\tvalid_0's l1: 5.88459\n[200]\tvalid_0's l1: 5.86182\n[300]\tvalid_0's l1: 5.85198\n[400]\tvalid_0's l1: 5.84547\n[500]\tvalid_0's l1: 5.84063\n[600]\tvalid_0's l1: 5.83786\n[700]\tvalid_0's l1: 5.83575\n[800]\tvalid_0's l1: 5.83421\n[900]\tvalid_0's l1: 5.83328\n[1000]\tvalid_0's l1: 5.83264\n[1100]\tvalid_0's l1: 5.83201\n[1200]\tvalid_0's l1: 5.83182\n[1300]\tvalid_0's l1: 5.83155\n[1400]\tvalid_0's l1: 5.8313\n[1500]\tvalid_0's l1: 5.83128\n[1600]\tvalid_0's l1: 5.83127\nEarly stopping, best iteration is:\n[1590]\tvalid_0's l1: 5.83122\nMAE : 5.8312171622703675\n","output_type":"stream"}]},{"cell_type":"code","source":"# Submission\n\nimport optiver2023\nenv = optiver2023.make_env()\niter_test = env.iter_test()\n\n\n\ncounter = 0\n\n\n\ncounter = 0\nfor (test, revealed_targets, sample_prediction) in iter_test:\n    if counter == 0:\n        print(test.head(3))\n        print(revealed_targets.head(3))\n        print(sample_prediction.head(3))\n    test=test.drop('currently_scored',axis=1)\n    test=generate_all_features(test)\n    sample_prediction['target'] = lgb_model.predict(test)\n    env.predict(sample_prediction)\n    counter += 1\n\nprint('Subimssion is completed')","metadata":{"execution":{"iopub.status.busy":"2024-10-21T11:02:27.965367Z","iopub.execute_input":"2024-10-21T11:02:27.965764Z","iopub.status.idle":"2024-10-21T11:03:18.113758Z","shell.execute_reply.started":"2024-10-21T11:02:27.965727Z","shell.execute_reply":"2024-10-21T11:03:18.112459Z"},"trusted":true},"execution_count":11,"outputs":[{"name":"stdout","text":"This version of the API is not optimized and should not be used to estimate the runtime of your code on the hidden test set.\n   stock_id  date_id  seconds_in_bucket  imbalance_size  \\\n0         0      478                  0      3753451.43   \n1         1      478                  0       985977.11   \n2         2      478                  0       599128.74   \n\n   imbalance_buy_sell_flag  reference_price  matched_size  far_price  \\\n0                       -1         0.999875   11548975.43        NaN   \n1                       -1         1.000245    3850033.97        NaN   \n2                        1         1.000584    4359198.25        NaN   \n\n   near_price  bid_price  bid_size  ask_price  ask_size  wap   row_id  \\\n0         NaN   0.999875  22940.00   1.000050   9177.60  1.0  478_0_0   \n1         NaN   0.999940   1967.90   1.000601  19692.00  1.0  478_0_1   \n2         NaN   0.999918   4488.22   1.000636  34955.12  1.0  478_0_2   \n\n   currently_scored  \n0             False  \n1             False  \n2             False  \n   stock_id  date_id  seconds_in_bucket  revealed_target  revealed_date_id  \\\n0         0      478                  0        -2.310276               477   \n1         1      478                  0       -12.850165               477   \n2         2      478                  0        -0.439882               477   \n\n   revealed_time_id  \n0             26235  \n1             26235  \n2             26235  \n    row_id  target\n0  478_0_0     0.0\n1  478_0_1     0.0\n2  478_0_2     0.0\nSubimssion is completed\n","output_type":"stream"}]}]}