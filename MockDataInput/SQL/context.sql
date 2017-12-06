CREATE TABLE context_tb (
    "id"         INTEGER PRIMARY KEY AUTOINCREMENT,
    "name"       VARCHAR(127) UNIQUE,
    "apply"      VARCHAR(15)  NOT NULL DEFAULT "hdr",
    "dir"        INTEGER               DEFAULT 0,
    "datatype"   VARCHAR(15)  NOT NULL DEFAULT "string",
    "precapture" VARCHAR(15),
    "necessary"  TINYINT               DEFAULT 0 CHECK (necessary < 2),
    "multiple"   TINYINT               DEFAULT 0 CHECK (multiple < 2),
    "pattern"    VARCHAR(255),
    "dft_value"  VARCHAR(15)
);
-- count: 9
-- prefix: NULL

-- NOTE: context must be append to the last.
-- name                        || apply  || d || DT       || pre          || nec || mul || pattern                      || dft
T: 'http_req_method'           || 'hdr'  || 0 || 'string' || ''           || 0   || 0   || '^GET$|^POST$|^PUT$|^PATCH$|^DELETE$|^OPTIONS$|^HEAD$|^BITS_POST$|^PROPFIND$|^PROPPATCH$|^REPORT$|^ACE$|^CONNECT$'
T: 'http_req_url'              || 'hdr'  || 0 || 'string' || ''           || 0   || 0
T: 'http_req_host_url'         || 'hdr'  || 0 || 'string' || ''           || 0   || 0
T: 'http_req_param'            || 'hdr'  || 0 || 'string' || 'url_decode' || 0   || 0
T: 'http_req_params'           || 'hdr'  || 0 || 'string' || ''           || 0   || 0
T: 'http_rsp_code'             || 'hdr'  || 1 || 'string' || ''           || 0   || 0
T: 'http_rsp_latency'          || 'hdr'  || 1 || 'int'    || ''           || 0   || 0
T: 'http_req_body'             || 'body' || 0 || 'string' || ''           || 0   || 0
T: 'http_rsp_body'             || 'body' || 1 || 'string' || ''           || 0   || 0
T: 'http_req_form'             || 'body' || 0 || 'string' || 'url_decode' || 0   || 0
T: 'http_req_forms'            || 'body' || 0 || 'string' || ''           || 0   || 0
T: 'http_req_upfile_names'     || 'body' || 0 || 'string' || ''           || 0   || 0
T: 'http_req_upfile_name'      || 'body' || 0 || 'string' || 'url_decode' || 0   || 1
T: 'http_req_upfile_cont'      || 'body' || 0 || 'string' || ''           || 0   || 1
T: 'http_req_upfile_hash'      || 'body' || 0 || 'string' || ''           || 0   || 1
T: 'http_req_upfile_size'      || 'body' || 0 || 'int'    || ''           || 0   || 1
T: 'http_req_upfile_type'      || 'body' || 0 || 'string' || ''           || 0   || 1
T: 'http_req_upfile'           || 'body' || 0 || 'string' || ''           || 0   || 0
T: 'http_rsp_downfile_name'    || 'hdr'  || 1 || 'string' || 'url_decode' || 0   || 0
T: 'http_rsp_downfile_cont'    || 'body' || 1 || 'string' || ''           || 0   || 0
T: 'http_rsp_downfile_hash'    || 'body' || 1 || 'string' || ''           || 0   || 0
T: 'http_rsp_downfile_size'    || 'body' || 1 || 'int'    || ''           || 0   || 0
T: 'http_rsp_downfile_type'    || 'body' || 1 || 'string' || ''           || 0   || 0
T: 'http_user_token'           || 'hdr'  || 0 || 'string' || ''           || 0   || 0
T: 'http_login_name'           || 'hdr'  || 0 || 'string' || ''           || 0   || 0
T: 'http_req_host'             || 'hdr'  || 0 || 'string' || ''           || 0   || 0   || 'host:'
T: 'http_req_uagent'           || 'hdr'  || 0 || 'string' || 'url_decode' || 1   || 0   || 'user-agent:'                || 'n'
T: 'http_req_refer'            || 'hdr'  || 0 || 'string' || ''           || 1   || 0   || 'referer:'                   || '0'
T: 'http_req_cookie'           || 'hdr'  || 0 || 'string' || 'url_decode' || 0   || 0
T: 'http_req_cookies'          || 'hdr'  || 0 || 'string' || ''           || 0   || 0   || 'cookie:|cookie2:'
T: 'http_req_auth'             || 'hdr'  || 0 || 'string' || ''           || 0   || 0   || 'authorization:'
T: 'http_req_auth_decode_1'    || 'hdr'  || 0 || 'string' || 'url_decode' || 0   || 0
-- 'http_req_auth_decode_2'    || 'hdr'  || 0 || 'string' || ''           || 0   || 0
T: 'http_req_cont_len'         || 'hdr'  || 0 || 'int'    || ''           || 0   || 0   || 'content-length:'
T: 'http_rsp_cont_len'         || 'hdr'  || 1 || 'int'    || ''           || 0   || 0   || 'content-length:'
T: 'http_req_x_file_name'      || 'hdr'  || 0 || 'string' || ''           || 0   || 0   || 'x-file-name:'
T: 'http_req_x_file_size'      || 'hdr'  || 0 || 'string' || ''           || 0   || 0   || 'x-file-size:'
T: 'http_rsp_location'         || 'hdr'  || 1 || 'string' || ''           || 1   || 0   || 'location:'                  || '0'
T: 'http_req_cont_disp'        || 'hdr'  || 0 || 'string' || ''           || 0   || 0   || 'content-disposition:'
T: 'http_rsp_cont_disp'        || 'hdr'  || 1 || 'string' || ''           || 0   || 0   || 'content-disposition:'
T: 'http_req_bits_packet_type' || 'hdr'  || 0 || 'string' || ''           || 0   || 0   || 'bits-packet-type:'
T: 'http_rsp_etag'             || 'hdr'  || 1 || 'string' || ''           || 0   || 0   || 'etag:'
T: 'http_req_cont_type'        || 'hdr'  || 0 || 'string' || ''           || 1   || 0   || 'content-type:'              || 'n'
T: 'http_rsp_cont_type'        || 'hdr'  || 1 || 'string' || ''           || 1   || 0   || 'content-type:'              || 'n'
T: 'http_req_trans_encoding'   || 'hdr'  || 0 || 'string' || ''           || 0   || 0   || 'transfer-encoding:'
T: 'http_rsp_trans_encoding'   || 'hdr'  || 1 || 'string' || ''           || 0   || 0   || 'transfer-encoding:'
T: 'http_req_soap_action'      || 'hdr'  || 0 || 'string' || ''           || 0   || 0   || 'soapaction:'
T: 'http_rsp_rawcookie'        || 'hdr'  || 1 || 'string' || ''           || 0   || 0   || 'set-cookie:'
T: 'http_rsp_cookie'           || 'hdr'  || 1 || 'string' || 'url_decode' || 0   || 0
T: 'http_rsp_cookies'          || 'hdr'  || 1 || 'string' || ''           || 0   || 0
T: 'http_rsp_cont_encoding'    || 'hdr'  || 1 || 'string' || ''           || 0   || 0   || 'content-encoding:'
T: 'http_req_xrequested_with'  || 'hdr'  || 0 || 'string' || ''           || 0   || 0   || 'x-requested-with:'
T: 'http_req_cont_range'       || 'hdr'  || 0 || 'string' || ''           || 0   || 0   || 'content-range:'
T: 'http_rsp_cont_range'       || 'hdr'  || 1 || 'string' || ''           || 0   || 0   || 'content-range:'
T: 'http_req_range_start'      || 'hdr'  || 0 || 'string' || ''           || 1   || 0   || ''                           || '0'
T: 'http_rsp_range_start'      || 'hdr'  || 1 || 'string' || ''           || 1   || 0   || ''                           || '0'
T: 'http_rsp_google_accounts'  || 'hdr'  || 1 || 'string' || ''           || 0   || 0   || 'google-accounts-signin:'
T: 'http_rsp_hsts'             || 'hdr'  || 1 || 'string' || ''           || 0   || 0   || 'strict-transport-security:'
T: 'mail_sub_type'             || 'hdr'  || 0 || 'string' || ''           || 0   || 0
T: 'mail_username'             || 'hdr'  || 0 || 'string' || ''           || 0   || 0
T: 'mail_sender'               || 'hdr'  || 1 || 'array'  || ''           || 0   || 0
T: 'mail_recvers'              || 'hdr'  || 1 || 'array'  || ''           || 0   || 0
T: 'login_result'              || 'hdr'  || 1 || 'bool'   || ''           || 0   || 0
T: 'mail_recv_file_name'       || 'hdr'  || 1 || 'string' || 'url_decode' || 0   || 1
T: 'mail_recv_file_cont'       || 'hdr'  || 1 || 'string' || ''           || 0   || 1
T: 'mail_recv_file_hash'       || 'hdr'  || 1 || 'string' || ''           || 0   || 1
T: 'mail_recv_file_size'       || 'hdr'  || 1 || 'int'    || ''           || 0   || 1
T: 'mail_recv_file_type'       || 'hdr'  || 1 || 'string' || ''           || 0   || 1
T: 'mail_send_file_names'      || 'hdr'  || 0 || 'string' || ''           || 0   || 0
T: 'mail_send_file_name'       || 'hdr'  || 0 || 'string' || 'url_decode' || 0   || 1
T: 'mail_send_file_cont'       || 'hdr'  || 0 || 'string' || ''           || 0   || 1
T: 'mail_send_file_hash'       || 'hdr'  || 0 || 'string' || ''           || 0   || 1
T: 'mail_send_file_size'       || 'hdr'  || 0 || 'int'    || ''           || 0   || 1
T: 'mail_send_file_type'       || 'hdr'  || 0 || 'string' || ''           || 0   || 1
T: 'mail_send_file'            || 'hdr'  || 0 || 'string' || ''           || 0   || 0
T: 'http_req_origin'           || 'hdr'  || 0 || 'string' || ''           || 0   || 0   || 'origin:'
T: 'ssl_sni'                   || 'hdr'  || 0 || 'string' || ''           || 0   || 0

CREATE INDEX name_index on context_tb (name);
