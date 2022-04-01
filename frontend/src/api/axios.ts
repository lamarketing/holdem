import axios from "axios";
import {api_url} from "@/api/api_url";

/**
 * Общая функция запроса к API
 * @param url
 * @param params
 */
async function getZ(url: string, params: object | null = null) {
  let res
  await axios.get(
    api_url + url + "/",
    {
      params: params
    }).then(
    (response) => res = response.data
  ).catch(
    (error) => res = {error: error}
  )
  return res
}


async function postZ(url: string, data: object | null = null) {
  let res: any
  await axios({
    method: 'post',
    url: api_url + url + "/",
    data: data
  }).then(
    (response) => res = response.data
  ).catch(
    () => res = null
  )
  return res
}


export {
  getZ,
  postZ
}