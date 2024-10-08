import request from './request';

const baseUrl = process.env.VUE_APP_API_URL;

export interface ProjectDetail {
    images: string[]
    title: string
    dict: string
    project: {
        height: number
        width: number
    },
    bgm: string,
    voice: string,
    textArr: Array<textItem>
}


export interface textItem {
    bgi?: string
    text?: string
    bgc?: string
    fontSize?: number
    marginBottom?: number
    color?: string
}

export function getProjectDetail(data: { projectName: string }): Promise<ProjectDetail> {
    return request<ProjectDetail>({
        method: 'post',
        url: `${baseUrl}/getProjectDetail`,
        payload: data
    }).then(response => response.data);
}

export function getImagePackage(data: { projectName: string }): Promise<{ images: string[] }> {
    return request<{ images: string[] }>({
        method: 'get',
        url: `${baseUrl}/get_project_images/${data.projectName}`,
    }).then(response => response.data);
}


export function savePorject(data: { projectName: string, ProjectDetail: ProjectDetail }): Promise<{ images: string[] }> {
    return request<{ images: string[] }>({
        method: 'post',
        url: `${baseUrl}/save_project/${data.projectName}`,
        payload: {
            detail: data.ProjectDetail
        }
    }).then(response => response.data);
}

export function MakeEveryVideo(data: { projectName: string }): Promise<any> {
    return request<any>({
        method: 'post',
        url: `${baseUrl}/makeMovie`,
        payload: data
    }).then(response => response.data);
}

export function mergeVideo(data: { projectName: string }): Promise<any> {
    return request<any>({
        method: 'post',
        url: `${baseUrl}/mergeVideo`,
        payload: data
    }).then(response => response.data);
}


export function makeMovie(data: { projectName: string }): Promise<any> {
    return request<any>({
        method: 'post',
        url: `${baseUrl}/makeMovie`,
        payload: data
    }).then(response => response.data);
}

export function getAllBGM(): Promise<any> {
    return request<any>({
        method: 'get',
        url: `${baseUrl}/bgm_list`,
    }).then(response => response.data);
}

export function getAllvoicelist(): Promise<any> {
    return request<any>({
        method: 'get',
        url: `${baseUrl}/voicelist`,
    }).then(response => response.data);
}

