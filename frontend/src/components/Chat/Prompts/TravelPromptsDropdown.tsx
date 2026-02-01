/**
 * Copyright AGNTCY Contributors (https://github.com/agntcy)
 * SPDX-License-Identifier: Apache-2.0
 **/

import React, { useState, useRef, useEffect } from "react"
import LoadingSpinner from "./LoadingSpinner"
import { PromptCategory } from "./PromptTypes"

// Travel-specific suggested prompts
const TRAVEL_PROMPTS: PromptCategory[] = [
  {
    name: "popular_destinations",
    prompts: [
      {
        prompt: "Plan a trip to Paris with budget $800 on 2026-03-10",
        description: "Romantic getaway to the City of Lights"
      },
      {
        prompt: "Find flights to Tokyo with a $1200 budget for 2026-04-15",
        description: "Experience Japanese culture and cuisine"
      },
      {
        prompt: "Search for flight options to London, budget $600, departing 2026-05-01",
        description: "Explore historic landmarks and British culture"
      },
    ]
  },
  {
    name: "budget_travel",
    prompts: [
      {
        prompt: "Plan a trip to Rome with budget $500 on 2026-03-20",
        description: "Ancient history on a budget"
      },
      {
        prompt: "Find cheap flights to Barcelona for $400 on 2026-06-01",
        description: "Beach and architecture without breaking the bank"
      },
    ]
  },
  {
    name: "luxury_travel",
    prompts: [
      {
        prompt: "Plan a luxury trip to Dubai with budget $3000 on 2026-04-01",
        description: "Experience world-class luxury and shopping"
      },
      {
        prompt: "Find premium flights to Sydney with budget $2500 for 2026-05-15",
        description: "Explore Australia in comfort"
      },
    ]
  }
]

interface TravelPromptsDropdownProps {
  visible: boolean
  onSelect: (query: string) => void
  pattern?: string
}

const TravelPromptsDropdown: React.FC<TravelPromptsDropdownProps> = ({
  visible,
  onSelect,
  pattern,
}) => {
  const [isOpen, setIsOpen] = useState(false)
  const [categories, setCategories] = useState<PromptCategory[]>(TRAVEL_PROMPTS)
  const dropdownRef = useRef<HTMLDivElement>(null)
  const [isLoading, setIsLoading] = useState(false)

  // Handle outside clicks and escape key
  useEffect(() => {
    if (!visible || !isOpen) return

    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false)
      }
    }

    const handleEscapeKey = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        setIsOpen(false)
      }
    }

    document.addEventListener("mousedown", handleClickOutside, true)
    document.addEventListener("keydown", handleEscapeKey)

    return () => {
      document.removeEventListener("mousedown", handleClickOutside, true)
      document.removeEventListener("keydown", handleEscapeKey)
    }
  }, [visible, isOpen])

  const handleToggle = () => setIsOpen(!isOpen)

  const handleItemClick = (item: string) => {
    onSelect(item)
    setIsOpen(false)
  }

  if (!visible) return null

  const dropdownClasses = `flex h-9 w-166 cursor-pointer flex-row items-center gap-1 rounded-lg bg-chat-background p-2 transition-colors duration-200 ease-in-out hover:bg-chat-background-hover ${
    isOpen ? "bg-chat-background-hover" : ""
  }`

  const hasNoPrompts = categories.every((category) => category.prompts.length === 0)

  const menuClasses = `absolute bottom-full left-0 z-[1000] mb-1 max-h-[365px] min-h-[50px] w-[320px] overflow-y-auto rounded-[6px] border border-nav-border bg-chat-dropdown-background px-[2px] py-0 opacity-100 shadow-[0px_2px_5px_0px_rgba(0,0,0,0.05)] ${
    isOpen ? "block animate-fadeInDropdown" : "hidden"
  }`

  const iconClasses = `absolute bottom-[36.35%] left-[26.77%] right-[26.77%] top-[36.35%] bg-chat-dropdown-icon transition-transform duration-300 ease-in-out ${
    isOpen ? "rotate-180" : ""
  }`

  const getCategoryTitle = (name: string): string => {
    switch (name) {
      case "popular_destinations":
        return "✈️ POPULAR DESTINATIONS"
      case "budget_travel":
        return "💰 BUDGET TRAVEL"
      case "luxury_travel":
        return "✨ LUXURY TRAVEL"
      default:
        return name.toUpperCase().replace("_", " ")
    }
  }

  return (
    <div className="flex items-center gap-3">
      <div className="relative inline-block" ref={dropdownRef}>
        <div className={dropdownClasses} onClick={handleToggle}>
          <div className="order-0 flex h-5 w-122 flex-none flex-grow-0 flex-col items-start gap-1 p-0">
            <div className="order-0 h-5 w-122 flex-none flex-grow-0 self-stretch whitespace-nowrap font-cisco text-sm font-normal leading-5 text-chat-text">
              ✈️ Trip Ideas
            </div>
          </div>
          <div className="relative order-1 h-6 w-6 flex-none flex-grow-0">
            <div
              className={iconClasses}
              style={{ clipPath: "polygon(50% 100%, 0% 0%, 100% 0%)" }}
            />
          </div>
        </div>

        <div className={menuClasses}>
          {isLoading || hasNoPrompts ? (
            <LoadingSpinner message="Loading travel suggestions..." />
          ) : (
            categories.map((category, index) => (
              <div key={`category-${index}`} className="px-2 py-2">
                <div className="mb-2 h-[36px] w-full gap-2 bg-chat-dropdown-background pb-2 pl-[10px] pr-[10px] pt-2 font-cisco text-sm font-normal leading-5 tracking-[0%] text-chat-text opacity-60">
                  {getCategoryTitle(category.name)}
                </div>
                {category.prompts.map((item, idx) => (
                  <div
                    key={`prompt-${index}-${idx}`}
                    className="flex mx-0.5 my-0.5 flex-col min-h-10 w-[calc(100%-4px)] cursor-pointer items-center bg-chat-dropdown-background px-2 py-[6px] transition-colors duration-200 ease-in-out hover:bg-chat-background-hover gap-y-1.5 border-t border-gray-400 border-opacity-20"
                    onClick={() => handleItemClick(item.prompt)}
                  >
                    <div className="w-full break-words font-cisco text-sm font-normal leading-5 tracking-[0%] text-chat-text">
                      {item.prompt}
                    </div>
                    {item.description && (
                      <div className="w-full break-words font-cisco text-xs font-normal leading-4 tracking-[0%] text-chat-text opacity-70">
                        {item.description}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  )
}

export default TravelPromptsDropdown
