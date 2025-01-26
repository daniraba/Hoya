import { Checkbox } from "./ui/checkbox"
import {
    Command,
    CommandEmpty,
    CommandGroup,
    CommandInput,
    CommandItem,
    CommandList,
  } from "@/components/ui/command"
  import {
    Popover,
    PopoverContent,
    PopoverTrigger,
  } from "@/components/ui/popover"

import { useRouter } from "@node_modules/next/navigation"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"

function Prediction({
    type,
    isReportCorrect,
    setReportCorect,
    newType,
    setNewType,
    handleSubmit,
    post,
    isSubmitting,
    submittedData
}){

    const router = useRouter()

    return (
        <>
        <div
        className="w-3/4 border border-gray-300 rounded-xl bg-white/[0.6]"
        >
            <div className="px-8 py-4">
                <h1 className="text-2xl font-bold ">
                    Your Diagnosis Report
                </h1>
            </div>
            <div
            className="mt-12 mx-12 pb-12 font-bold flex-center gap-12 text-4xl border-b border-zinc-400 "
            >
                <span>{type === 0 ? ('You do not have diabetes') : (`You have Type ${type} Diabetes`)}</span>
                <div
                    className="text-base font-bold mx-12 mt-8 text-gray-600"
                    >
                        If this report does not match with your doctor's diagnosis, we highly recommend that you take another
                        report from a doctor
                    </div>
            </div>



            <div
            className="text-xl font-bold mx-12 mt-8"
            >
                You can help improve our diagnosis by uploading your data...
            </div>

            <div
            className="flex-start mt-2 mx-12 gap-4"
            >
                <p className="text-sm">
                    Was the diagnosis from our website different from your doctor's even after rediagnosing?
                </p>
                <Checkbox
                checked = {isReportCorrect}
                onCheckedChange= {(check) => {
                    setReportCorect(check)
                }}
                />
            </div>

            <div
            className="w-full"
            >
            {isReportCorrect ? (
                <div
                className="mx-12 my-4 border border-zinc-300 px-8 py-4 rounded-xl"
                >
                <p className="font-inter text-sm mb-4">
                    Please specify what was the actual type
                </p>
                <RadioGroup defaultValue={newType} onValueChange={(value) => {
                    setNewType(value.toString())
                    console.log(post, newType)
                    }}>
                    <div className="flex items-center gap-2">
                    <RadioGroupItem value='0'/>
                    <h1 className="text-sm font-semibold ">
                        No Diabetes
                    </h1>
                    </div>
                    <div className="flex items-center gap-2">
                    <RadioGroupItem value='1'/>
                    <h1 className="text-sm font-semibold ">
                        Diabetes Type 1
                    </h1>
                    </div>
                    <div className="flex items-center gap-2">
                    <RadioGroupItem value='2'/>
                    <h1 className="text-sm font-semibold ">
                        Diabetes Type 2
                    </h1>
                    </div>
                </RadioGroup>
                </div>
            ) : 
               null 
            }
            
            <div className="flex-between mx-12 my-8">
                <button
                className="outline_btn"
                onClick={() => router.push()}
                >
                    Ignore
                </button>
                <button
                className="black_btn"
                type='submit'
                disabled={isSubmitting || submittedData}
                onClick={() => handleSubmit()}
                >
                   {isSubmitting ? 'Submitting' : (submittedData ? 'Submitted' : 'Submit')}
                </button>
            </div>
            </div>

        </div>
        </>
    ) 
}
export default Prediction