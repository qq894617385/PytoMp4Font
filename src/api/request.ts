import axios, { AxiosRequestConfig, AxiosResponse, Method } from 'axios';

// 请求参数接口
interface RequestParams<T> {
    method: Method;
    url: string;
    payload?: any;
    config?: AxiosRequestConfig;
}

// 响应数据接口
interface ApiResponse<T> {
    data: T;
}

// 通用请求函数
const request = <T>({
    method,
    url,
    payload,
    config
}: RequestParams<T>): Promise<ApiResponse<T>> => {
    const requestConfig: AxiosRequestConfig = {
        method,
        url,
        ...config,
        headers: { ...config?.headers }
    };

    if (method === 'GET') {
        requestConfig.params = payload;
    } else {
        requestConfig.data = payload;
    }

    return axios(requestConfig)
        .then((response: AxiosResponse<ApiResponse<T>>) => response.data)
        .catch((error: any) => {
            throw error;
        });
};

export default request;
