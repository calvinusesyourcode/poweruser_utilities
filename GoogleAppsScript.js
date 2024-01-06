const init_time = new Date()
const f_datetime = Utilities.formatDate(init_time, "America/Vancouver", "yyyy/MM/dd H:mm:ss")

// user values
const openai_key = "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"
// const assistant_id = "asst_rhmXsyeXVrfisVnu34zd2AsD"
const assistant_id = "asst_IcTfl2zZgUuwOgytW8se5nRh"
const headers = 1

const sheet_schema = {
  ".threads": ["init", "last_msg", "phone_number", "name", "thread_id"],
  ".thread_log": ["thread_id", "reply"],
  ".assistant_files": ["date", "file_id", "purpose"]
}

// global constants
const openai_assistant_headers = {
  'Authorization': `Bearer ${openai_key}`,
  'Content-Type': 'application/json',
  'OpenAI-Beta': 'assistants=v1'
}

// init global variables
let sheet_id = null


// main
function doPost(e) { // runs when a POST request is received to our deployed web app endpoint https://scripts.google.com/...<script_id>.../exec
  let data = {}

  if (e.postData) { // get JSON body
    data = JSON.parse(e.postData.contents);
  }

  if (e.parameter) { // get URL-encoded params
    Object.keys(e.parameter).forEach((key) => {
      data[key] = e.parameter[key]
    })
  }

  if (!data.sheet_id) { // "sheet_id" is the ID of the Google Sheet that this script is bound to https://docs.google.com/spreadsheets/d/...<sheet_id>.../edit
    throw("ERROR: !data.sheet_id")
  }
  sheet_id = data.sheet_id

  if (!data.fn) { // "fn" is what I decided to call the action to perform
    throw("ERROR: !data.fn")
  }

  if (data.date === undefined || data.date == "") {data.date = f_datetime}
  else {data.date = Utilities.formatDate(new Date(data.date), "America/Vancouver", "yyyy/MM/dd H:mm:ss")}

  if (data.fn == "debug") {
    return ContentService.createTextOutput(`e = ${JSON.stringify(e)}`)
  }
  
  if (data.fn == "file_upload") {
    if (!data.file_base64 || !data.file_purpose) {
      throw new Error("ERROR: !data.file_base64 OR !data.file_purpose")
    }

    const ss = SpreadsheetApp.openById(sheet_id).getSheetByName(sheet_setup(".assistant_files", sheet_id))
    const file_id = upload_file(data.file_purpose.replace(/[^a-zA-Z0-9]/g, '').substring(0, 20), data.file_base64, "assistants").id
    ss.appendRow([f_datetime, file_id, data.file_purpose])
    return ContentService.createTextOutput(file_id)
  }

  if (data.fn == "msg_assistant") {
    if (!data.message || !data.phone_number || !data.name) {
      throw new Error("ERROR: !data.message OR !data.phone_number OR !data.name")
    }

    return ContentService.createTextOutput(msg_assistant(data.sheet_id, data.message, data.phone_number, data.name))
  }

  if (data.fn == "assist") {
    if (!data.message) {
      throw new Error("ERROR: !data.message")
    }
    let file_ids = []
    let message = data.message.toString()
    if (data.file_ids_text) {
      file_ids = data.file_ids_text.split(";")
      message = `regarding the ${file_ids.length} attached files, ${data.message.toString()}`
    }
    return ContentService.createTextOutput(msg_assistant(message, "123456789", "admin", file_ids))
  }

  if (data.fn == "smart_data_entry") {
    if (!data.data_string) {
      throw new Error("ERROR: !data.data_string")
    }
    return ContentService.createTextOutput(handle_smart_data(sheet_id, data))
  }

  return ContentService.createTextOutput("ERROR? Nothing happened...\n"+JSON.stringify(data))
}
function doGet(e) {
  return ContentService.createTextOutput("Beep boop!")
}


// the juice of the smoothie
function msg_assistant(input_message, phone_number, name, file_ids=[]) {
  const sheetname = sheet_setup(".threads", sheet_id)
  const ss = SpreadsheetApp.openById(sheet_id).getSheetByName(sheetname)
  phone_number = fix_number(phone_number)

  const existing_thread_data = ss.getRange(headers+1,1,ss.getLastRow(),ss.getLastColumn()).getValues()
  .map(row => Object.fromEntries(sheet_schema[".threads"].map((key, index) => [key, row[index]])));
  let existing_user_thread = null
  let thread_id = null
  let thread_row_number = null
  let last_row = ss.getLastRow()
  for (let i = 0, l = ss.getLastRow(); i < l; i++) {
    if (existing_thread_data[i]["phone_number"] == phone_number) {
      existing_user_thread = existing_thread_data[i]
      thread_row_number = i+1+headers
    }
  }

  if (!existing_user_thread) {
    thread_id = create_new_thread_with_messages(input_message, file_ids).id
    ss.appendRow([f_datetime, f_datetime, phone_number, name, thread_id]) 
  } else {
    thread_id = existing_user_thread["thread_id"]
    ss.getRange(thread_row_number,sheet_schema[".threads"].indexOf("last_msg")+1).setValue(Utilities.formatDate(new Date(), "America/Vancouver", "yyyy/MM/dd H:mm:ss"))
    console.log(append_message_to_thread(thread_id, input_message, file_ids))
  }
  let run = wait_on_run(assistant_id, thread_id)
  const messages = get_thread_messages(thread_id).data.map((msg)=>msg.id)
  const reply = read_message(thread_id, messages[0]).content[0].text.value
  const thread_log = sheet_setup(".thread_log",sheet_id)
  SpreadsheetApp.openById(sheet_id).getSheetByName(thread_log).appendRow([thread_id, reply])
  // spend_time_typing(reply)
  return reply
}


// helpers
function log(message, level="error", ) {
    console.error(message)
    SpreadsheetApp.openById(sheet_id).getSheetByName(sheet_setup(".appscript_log", sheet_id)).appendRow([f_datetime, level, message])
}
function fetch(method, endpoint, payload, headers=openai_assistant_headers, throw_error=true) {
  try {
    return JSON.parse(UrlFetchApp.fetch(endpoint, {
      method: method,
      headers: headers,
      payload: method == "POST" ? payload : null,
    }))
  } catch (error) {
    log(`Error fetching ${endpoint} with ${method} method: ${error}`, sheet_id)
    if (throw_error) throw error
  }
}
function spend_time_typing(message) {
  const time_to_type = message.length * (60 + (40 * Math.random()))
  const estimated_extra_time = 3000
  const time_since = Date.now().valueOf()-init_time.valueOf()
  const time_to_wait = time_to_type - (estimated_extra_time + time_since)
  if (time_to_wait > 50) {
    console.log(`Waiting ${Math.floor(time_to_wait/1000)} seconds...`)
    Utilities.sleep(Math.floor(time_to_wait))
  }
  return true
}
function sheet_setup(app, sheet_id) {
  const sheetname = app.includes("---") ? app.slice(0,app.indexOf("---")) : app;
  if (!sheet_schema[sheetname]) {
    throw(`ERROR: !sheet_schema["${sheetname}"]`)
  }
  if (!sheet_id) {
    throw("ERROR: no sheet_id");
  }
  if (SpreadsheetApp.openById(sheet_id).getSheetByName(sheetname) === null) {
    SpreadsheetApp.openById(sheet_id).insertSheet().setName(sheetname);
    if (Object.keys(sheet_schema).includes(sheetname)) {
      SpreadsheetApp.openById(sheet_id).getSheetByName(sheetname).getRange(1,1,1,sheet_schema[sheetname].length).setValues([sheet_schema[sheetname]])
    }
  }
  return sheetname
}
function fix_number(string) {
  return string.replace(/\D/g, '');
}


// openai assistant helpers
function start_run(assistant_id, thread_id) {
  return fetch("POST", `https://api.openai.com/v1/threads/${thread_id}/runs`, JSON.stringify({"assistant_id":assistant_id})) //start run
}
function fetch_run_status(thread_id, run_id) {
  return fetch("GET", `https://api.openai.com/v1/threads/${thread_id}/runs/${run_id}`) //get run status
}
function wait_on_run(assistant_id, thread_id) {
  let run = start_run(assistant_id, thread_id)
  let waited = 0
  while (run.status === "queued" || run.status === "in_progress") {
    Utilities.sleep(waited <= 6000 ? 2000 : 500);
    run = fetch_run_status(thread_id, run.id)
    console.log(run)
  }
  return run;
}
function create_new_thread_with_messages(initial_message, file_ids=[]) {
  return fetch("POST", "https://api.openai.com/v1/threads", JSON.stringify({messages: [{role: "user", content: initial_message, file_ids: file_ids}]}))
}
function append_message_to_thread(thread_id, new_message, file_ids=[]) {
  return fetch("POST", `https://api.openai.com/v1/threads/${thread_id}/messages`, JSON.stringify({role: "user", content: new_message, file_ids: file_ids}))
}
function get_thread_messages(thread_id) {
  return fetch("GET", `https://api.openai.com/v1/threads/${thread_id}/messages`)
}
function read_message(thread_id, message_id) {
  return fetch("GET", `https://api.openai.com/v1/threads/${thread_id}/messages/${message_id}`)
}


// openai file helpers
function delete_openai_files(file_list) {
  return file_list.forEach((file_id) => {
    return fetch("DELETE", `https://api.openai.com/v1/files/${file_id}`, null, {'Authorization': `Bearer ${openai_key}`})
  })
}
function upload_file(file_name, base64_bytes, purpose) {
  const boundary = "------WebKitFormBoundary" + new Date().getTime()
  const data =
    "--" + boundary + "\r\n" +
    `Content-Disposition: form-data; name="file"; filename="${file_name}"\r\n` +
    'Content-Type: application/octet-stream\r\n\r\n' +
    base64_bytes + "\r\n" +
    "--" + boundary + "\r\n" +
    'Content-Disposition: form-data; name="purpose"\r\n\r\n' +
    purpose + "\r\n" +
    "--" + boundary + "--";

  fetch("POST", "https://api.openai.com/v1/files", data, {
    'Authorization': 'Bearer ' + openai_key,
    'Content-Type': 'multipart/form-data; boundary=' + boundary,
    'OpenAI-Beta': 'assistants=v1',
  })
}
function list_openai_files() {
  return fetch("GET", `https://api.openai.com/v1/files`, null, {'Authorization': `Bearer ${openai_key}`})
}


// misc helpers
function test_msg_assistant() {
  console.log(msg_assistant("1_0IEy1DN5mbHsI29r3iGfII6pOzUCto3W83YUr_Eoo4","Hello Jereymi!", "16042198248", "Calvin"))
}
function uploadImageToOpenAI() {

  // const imagePath = "https://cdn-images-1.medium.com/v2/resize:fit:800/1*ACTdu02H5suUDOG5b-PzrA.jpeg"
  // const file_base64 = Utilities.base64Encode(UrlFetchApp.fetch(imagePath).getContent())
  // file_id = upload_file("testfile.jpg", file_base64, "assistants").id

}
function delete_test_files() {

  delete_openai_files(list_openai_files().data.reduce((result, file) => {if (file.filename == "image") result.push(file.id); return result}, []))
  console.log(list_openai_files())

}
function print_last_n_messages(thread_id="thread_VBNnHGuRvmedZHXfdp39b8Sn", n=7) {
  try {
    const allMessages = get_thread_messages(thread_id).data;
    const start = Math.max(0, allMessages.length - n);
    const lastNMessages = allMessages.slice(start);

    lastNMessages.forEach((msg, index) => {
      console.log(`Message ${start + index + 1}/${allMessages.length}:`);
      console.log(`Content: ${msg.content}`);
      if (msg.file_ids && msg.file_ids.length > 0) {
        console.log(`Attached file IDs: ${msg.file_ids.join(", ")}`);
      } else {
        console.log("No files attached to this message.");
      }
      console.log('---------------------------');
    });
  } catch (error) {
    console.error('Error printing last N messages:', error);
    throw error;
  }
}
function test() {
  console.log(get_thread_messages("thread_JE06DEc8ZjeYoELGqdv8KiqD").data)
}
