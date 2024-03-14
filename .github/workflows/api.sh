function invoke_tci_v1_rest_api() {
  local http_code="${1}"
  local path="${3}"

  curl -sS -w "\n%{http_code}" --location \
     "https://https://eu.api.cloud.tibco.com/tci/v1/oauth2/token/subscriptions/0/${path}" \
     --header "accept: application/json" \
     --header "Authorization: Bearer ${TCI_TOKEN}" \
     "${@:4}" > /tmp/$$.tmp

  test_and_remove_http_code "${http_code}" "" "${HTTP_NOEXIT}"
  rm /tmp/$$.tmp
}

function get_tci_token() {

  if [[ -n "${TCI_TOKEN-}" ]]; then
    local current_date
    current_date="$(date '+%Y-%m-%d-%H-%M-%S')"
    if [[ "${current_date}" < "${TCI_TOKEN_EXPIRE_DATE-}" ]]; then
      echoerr "Using cached TCI token"
      return
    else
      echoerr "TCI token has expired"
    fi
  fi

  echoerr "Getting TCI token"
  local response="$(
    curl -sS -w "\n%{http_code}" \
      "https://eu.api.cloud.tibco.com/tci/v1/oauth2/token" \
      --header "Content-Type: application/x-www-form-urlencoded" \
      --data "grant_type=client_credentials&scope=TCI&client_id=${DEV_TCI_CLIENT_ID}&client_secret=${DEV_TCI_CLIENT_SECRET}"
  )"

  response="$(test_and_remove_http_code "200" "${response}")"
  echoerr "Got TCI token"

  TCI_TOKEN="$(jq --raw-output '.access_token' <<<"${response}")"
  export TCI_TOKEN

  local expires_in
  expires_in=$(($(jq --raw-output '.expires_in' <<<"${response}") / 2))

  TCI_TOKEN_EXPIRE_DATE="$(date --date="+${expires_in} seconds" '+%Y-%m-%d-%H-%M-%S')"
  export TCI_TOKEN_EXPIRE_DATE
}
