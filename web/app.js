const scenarios = [
  {
    id: "dog_door_alert",
    title: "Dog hears footsteps near the door",
    pet: { name: "Mochi", species: "dog", breed: "Shiba Inu" },
    context: "the front door at 8:30 PM",
    classification: {
      label: "bark_alert",
      confidence: 0.88,
      evidence: ["high energy pattern consistent with alert barking"]
    },
    translation:
      "Mochi: Human, I have detected suspicious activity near the front door at 8:30 PM. Please investigate while I remain extremely brave."
  },
  {
    id: "cat_empty_bowl",
    title: "Cat complains near the food bowl",
    pet: { name: "Luna", species: "cat", breed: "British Shorthair" },
    context: "the kitchen food bowl",
    classification: {
      label: "meow_hungry",
      confidence: 0.8,
      evidence: ["bright spectral centroid suggests a sharp meow"]
    },
    translation:
      "Luna: Esteemed food provider, my bowl situation near the kitchen food bowl requires urgent executive attention."
  },
  {
    id: "cat_sofa_purr",
    title: "Cat purrs during sofa time",
    pet: { name: "Bean", species: "cat", breed: "Ragdoll" },
    context: "the sofa grooming session",
    classification: {
      label: "purr_happy",
      confidence: 0.88,
      evidence: ["low energy and low zero-crossing rate resemble a purr"]
    },
    translation:
      "Bean: Your service is acceptable. Continue the current comfort protocol near the sofa grooming session."
  },
  {
    id: "dog_vet_whine",
    title: "Dog waits outside the vet room",
    pet: { name: "Nova", species: "dog", breed: "Border Collie" },
    context: "the veterinary clinic waiting area",
    classification: {
      label: "whine_anxious",
      confidence: 0.8,
      evidence: ["longer sustained signal resembles a whine"]
    },
    translation:
      "Nova: I am not panicking, but I would appreciate emotional backup around the veterinary clinic waiting area."
  }
];

const select = document.querySelector("#scenarioSelect");
const petAvatar = document.querySelector("#petAvatar");
const petName = document.querySelector("#petName");
const petMeta = document.querySelector("#petMeta");
const chatLog = document.querySelector("#chatLog");
const labelText = document.querySelector("#labelText");
const confidenceText = document.querySelector("#confidenceText");
const evidenceText = document.querySelector("#evidenceText");
const translateButton = document.querySelector("#translateButton");

function populateScenarios() {
  scenarios.forEach((scenario) => {
    const option = document.createElement("option");
    option.value = scenario.id;
    option.textContent = scenario.title;
    select.appendChild(option);
  });
}

function selectedScenario() {
  return scenarios.find((scenario) => scenario.id === select.value) || scenarios[0];
}

function setPet(scenario) {
  petAvatar.textContent = scenario.pet.name.slice(0, 1);
  petName.textContent = scenario.pet.name;
  petMeta.textContent = `${scenario.pet.breed} · ${scenario.pet.species}`;
}

function addBubble(text, kind) {
  const bubble = document.createElement("div");
  bubble.className = `bubble ${kind}`;
  bubble.textContent = text;
  chatLog.appendChild(bubble);
  chatLog.scrollTop = chatLog.scrollHeight;
}

async function translateScenario() {
  const scenario = selectedScenario();
  setPet(scenario);
  addBubble(`Recording near ${scenario.context}...`, "owner");
  translateButton.disabled = true;
  translateButton.textContent = "Analyzing...";

  let payload = scenario;
  try {
    const response = await fetch(`http://127.0.0.1:8004/translate/${scenario.id}`, {
      method: "POST"
    });
    if (response.ok) {
      payload = await response.json();
    }
  } catch (error) {
    payload = scenario;
  }

  const classification = payload.classification;
  labelText.textContent = classification.label;
  confidenceText.textContent = Number(classification.confidence).toFixed(2);
  evidenceText.textContent = classification.evidence.join(" ");
  addBubble(payload.translation, "pet");

  translateButton.disabled = false;
  translateButton.textContent = "Record & Translate";
}

populateScenarios();
setPet(scenarios[0]);
labelText.textContent = scenarios[0].classification.label;
confidenceText.textContent = scenarios[0].classification.confidence.toFixed(2);
evidenceText.textContent = scenarios[0].classification.evidence[0];
addBubble("Tap Record & Translate to simulate a collar audio event.", "owner");
translateButton.addEventListener("click", translateScenario);
select.addEventListener("change", () => {
  chatLog.textContent = "";
  const scenario = selectedScenario();
  setPet(scenario);
  addBubble(`Ready for ${scenario.title}.`, "owner");
});
