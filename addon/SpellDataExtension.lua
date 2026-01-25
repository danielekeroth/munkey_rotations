local function EnsureList(t)
	-- Converts {"mouseover","focus"} → { targets = {...} }
	if t.targets then
		return t.targets
	end
	return t
end

local function AppendUnique(list, values)
	local seen = {}
	for _, v in ipairs(list) do
		seen[v] = true
	end
	for _, v in ipairs(values) do
		if not seen[v] then
			table.insert(list, v)
			seen[v] = true
		end
	end
end

local function MergeBinding(spellID, newTargets, newSpecs)
	local BT = MainAddon.SpellData.BindingTargets
	local entry = BT[spellID]

	-- No entry yet → create it
	if not entry then
		BT[spellID] = {
			targets = { unpack(newTargets or {}) },
			specs = newSpecs and { unpack(newSpecs) } or nil,
		}
		return
	end

	-- Normalize targets
	local targets = EnsureList(entry)
	AppendUnique(targets, newTargets or {})

	-- Normalize specs (if present)
	if newSpecs then
		entry.specs = entry.specs or {}
		AppendUnique(entry.specs, newSpecs)
	end

	-- If original entry was shorthand, preserve its shape
	if not entry.targets then
		entry.targets = targets
	end
end

function ApplyCustomBindings()
	if not _G.MainAddon then
		return false
	end
	if not MainAddon.SpellData or not MainAddon.SpellData.BindingTargets then
		return false
	end

	-- Paladin
	MergeBinding(96231, { "mouseover" }) -- Rebuke
	MergeBinding(213644, { "mouseover" }) -- Cleanse Toxins
	MergeBinding(391054, { "mouseover" }) -- Intercession

	-- Protection Paladin
	MergeBinding(31935, { "mouseover" }, { PALADIN_PROTECTION_SPECID }) -- Avengers Shield

	-- Holy Paladin
	MergeBinding(85673, { "focus", "mouseover", "player" }, { PALADIN_HOLY_SPECID, PALADIN_PROTECTION_SPECID }) -- Word of Glory
	MergeBinding(156322, { "focus", "mouseover", "player" }, { PALADIN_HOLY_SPECID, PALADIN_PROTECTION_SPECID }) -- Eternal Flame
	MergeBinding(7328, { "focus", "mouseover" }, { PALADIN_HOLY_SPECID }) -- Redemption

	return true
end

if ApplyCustomBindings() then
	return
else
	local f = CreateFrame("Frame")
	f:RegisterEvent("ADDON_LOADED")
	f:SetScript("OnEvent", function(self)
		if ApplyCustomBindings() then
			self:UnregisterAllEvents()
			self:SetScript("OnEvent", nil)
		end
	end)
end
