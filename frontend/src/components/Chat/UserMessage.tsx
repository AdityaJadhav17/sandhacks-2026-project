/**
 * Copyright AGNTCY Contributors (https://github.com/agntcy)
 * SPDX-License-Identifier: Apache-2.0
 **/

import React from "react"
import { User } from "lucide-react"

interface UserMessageProps {
  content: string
}

const UserMessage: React.FC<UserMessageProps> = ({ content }) => {
  return (
    <div className="flex w-full flex-row items-start gap-3">
      <div className="flex h-8 w-8 flex-none items-center justify-center rounded-full bg-gray-600">
        <User size={16} className="text-white" />
      </div>

      <div className="flex flex-1 flex-col items-start justify-center rounded p-1">
        <div className="whitespace-pre-wrap break-words font-inter text-sm font-normal leading-6 text-gray-100">
          {content}
        </div>
      </div>
    </div>
  )
}

export default UserMessage
