import request from './request';

const baseUrl = process.env.VUE_APP_API_URL;



// 假设 API 直接返回 NewsItem[] 的数据结构
export function getNewsList(): Promise<String[]> {
    return request<String[]>({
        method: 'get',
        url: `${baseUrl}/getProjectNameList`
    }).then(response => response.data); // 直接返回 NewsItem[]，已在request中处理好
}

export function deleteProject(data: { project_name: string }): Promise<{ images: string[] }> {
    return request<{ images: string[] }>({
        method: 'post',
        url: `${baseUrl}/delete_project`,
        payload: data
    }).then(response => response.data);
}


export function createProject(data: { project_name: string }): Promise<{ images: string[] }> {
    return request<{ images: string[] }>({
        method: 'post',
        url: `${baseUrl}/create_project`,
        payload: data
    }).then(response => response.data);
}