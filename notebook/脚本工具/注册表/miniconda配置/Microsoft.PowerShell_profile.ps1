function admin{
    Start-Process -FilePath 'wt' -Verb RunAs
}

function cda{
    # 固定语法
    [CmdletBinding()]
    # 参数声明
    param(
        [Parameter()]
        [string] $pyenv
    )
    # conda切换环境
    Try{
        conda activate "$pyenv"
    } Catch {
        powershell.exe -ExecutionPolicy ByPass -NoExit -Command "& 'C:\dev\envs\Miniconda3\shell\condabin\conda-hook.ps1' ; conda activate $pyenv "
    }
}
