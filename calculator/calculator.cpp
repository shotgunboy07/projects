#include <iostream>
#include <string>
using namespace std;

class better_str
{
    public:
    string* arr;
    int len;
    void print_arr(){
        for(int i=0; i<len; i++) cout << *(arr + i) << " ";
        puts("");
    }
};

string add0(string expression){
    string ret = "";
    for(int i=0; i<expression.length()-1; i++){
        if(expression[i] == '+' || '-'){
            if(i==0 || expression[i-1] < '0' || expression[i] > '9'){
                cout << "front : " << expression.substr(0,i) << ", back : " << expression.substr(i,expression.length()-i) << endl;
                ret += expression.substr(0,i);
                ret += '0';
                ret += expression.substr(i,expression.length()-i);
            }
        }
    }
    return ret;
}

better_str parse(string line){
    int num_operators = 0;
    int num_paranthesis = 0;
    for(int i=0; i<line.length(); i++){
        if (line[i] == '+' || line[i] == '-' || line[i] == '/' || line[i] == '*'){
            num_operators++;
        }
        else if(line[i] == '(' || line[i] == ')'){
            num_paranthesis++;
        }
    }

    better_str ret;

    ret.arr = new string[ 2*num_operators+ num_paranthesis + 1 ];
    ret.len = 2*num_operators + num_paranthesis + 1;

    int ret_idx = 0;
    string temp = "";
    
    for (int i=0; i< line.length(); i++){
        if (line[i] == '+' || line[i] == '-' || line[i] == '*' || line[i] == '/' || line[i] == '(' || line[i] == ')'){
            if ( temp != "" ) {
                ret.arr[ret_idx++] = temp;
            }
            ret.arr[ret_idx++] = line[i];
            temp = "";

        }
        else if ( (line[i] <= '9' && line[i] >= '0') || line[i] == '.' ){
            temp += line[i];
            if ( i == line.length() - 1 ) {
                ret.arr[ret_idx++] = temp;
            }
        }
    }
    return ret;
}


float one_calc(string* parsed){
    if( parsed[1] == "+" ){
        return stof(parsed[0]) + stof(parsed[2]);
    }
    else if ( parsed[1] == "-"){
        return stof(parsed[0]) - stof(parsed[2]);
    }
    else if ( parsed[1] == "*"){
        return stof(parsed[0]) * stof(parsed[2]);
    }
    else if ( parsed[1] == "/"){

        if( stof(parsed[2]) == 0 ){
            cout << "Error: Division by zero" << endl;
            return 0;
        }
        else if( stof(parsed[0]) == 0 ){
            return 0;
        }

        else if( stof(parsed[0]) / stof(parsed[2]) == int(stof(parsed[0]) / stof(parsed[2])) ) {
            return int(stof(parsed[0]) / stof(parsed[2]));
        }
        else{
            return stof(parsed[0]) / stof(parsed[2]);
        }   
        
    }
}


float multi_operator_calc(string line){

    better_str parsed = parse(line);

    for( int i = 1; i<parsed.len - 1; i++){
        if( parsed.arr[i] == "*" || parsed.arr[i] == "/" ){
            string* modified_line = new string[parsed.len - 2];
            for ( int j=0; j<parsed.len-2;j++){

                if(j<i-1){
                    modified_line[j] = parsed.arr[j];
                }

                else if(j == i-1){
                    string temp[3] = {parsed.arr[i-1], parsed.arr[i], parsed.arr[i+1]};
                    modified_line[j] = to_string(one_calc(temp));
                    //cout<< one_calc(temp) << endl;
                } 

                else{
                    modified_line[j] = parsed.arr[j+2];
                }

                //cout <<"i,j = " << i<<"," << j <<" ," <<"modified_line[j]: " << modified_line[j] << endl;
            }
            parsed.arr = modified_line;
            parsed.len -= 2;

            //delete [] modified_line;
            //cout << "modified: "; parsed.print_arr();
            i--;
        }
    }

    //cout << "after multiplication: "; 
    //parsed.print_arr();

    for( int i = 1; i<parsed.len - 1; i++){
        if( parsed.arr[i] == "+" || parsed.arr[i] == "-" ){
            string* modified_line = new string[parsed.len - 2];
            for ( int j=0; j<parsed.len-2;j++){

                if(j<i-1){
                    modified_line[j] = parsed.arr[j];
                }

                else if(j == i-1){
                    string temp[3] = {parsed.arr[i-1], parsed.arr[i], parsed.arr[i+1]};
                    modified_line[j] = to_string(one_calc(temp));
                    //cout<< one_calc(temp) << endl;
                    j=0;
                } 

                else{
                    modified_line[j] = parsed.arr[j+2];
                }

                //cout <<"i,j = " << i<<"," << j <<" ," <<"modified_line[j]: " << modified_line[j] << endl;
            }
            parsed.arr = modified_line;
            parsed.len -= 2;
            //cout << "modified: "; parsed.print_arr();
            i--;
        }
    }

    if( stof(parsed.arr[0]) == int(stof(parsed.arr[0]))){
        return int(stof(parsed.arr[0]));
    }
    else{
        return stof(parsed.arr[0]);
    }
    
    
}

float paranthesis_calc(string line){
    int open_paranthesis = 0;
    int close_paranthesis = 0;

    for (int i=0; i<line.length(); i++){
        if (line[i] == '(') open_paranthesis++;
        else if (line[i] == ')') close_paranthesis++;
    }

    if (open_paranthesis != close_paranthesis) {
        cout << "Error: Unmatched paranthesis" << endl;
        return 0;
    }

    if (open_paranthesis == 0) {
        return multi_operator_calc(line);
    }

    while (open_paranthesis > 0) {

        int start = -1;
        int end = -1;

        for (int i=0; i<line.length(); i++){
            if (line[line.length()-i-1] == '(') {
                start = line.length()-i-1;
                open_paranthesis--;
                break;
            }
        }

        for (int i=start; i<line.length(); i++){
            if (line[i] == ')') {
                end = i;
                close_paranthesis--;
                break;
            }
        }

        //cout << "start: " << start << " end: " << end << endl;

        string sub_expression = line.substr(start + 1, end - start - 1);

        //cout << "sub_expression: " << sub_expression << endl;

        float result = multi_operator_calc(sub_expression);

        //cout << "result: " << result << endl;

        line.replace(start, end - start + 1, to_string(result));
    }

    //cout << "final line: " << line << endl;

    return multi_operator_calc(line);
}

int main(){
    string user_input;
    getline(cin, user_input);
    //cout << paranthesis_calc(user_input) << endl;
    cout << add0(user_input);
}
    


