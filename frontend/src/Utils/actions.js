const API_URL = "http://10.142.42.247:5000";

export const mainRoute = () => {
  return fetch(`${API_URL}/`)
    .then((response) => response.json())
    .catch((error) => {
      console.error(error);
    });
};

export const generateResponse = (data) => {
  return fetch(`${API_URL}/api/response`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .catch((error) => {
      console.error(error);
    });
};

export const getClinicalTrials = () => {
  return fetch(`${API_URL}/api/clinicalTrials`)
    .then((response) => response.json())
    .catch((error) => {
      console.error(error);
    });
};
